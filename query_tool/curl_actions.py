import pycurl
import StringIO
import urllib
from user_input import UserInput as ui

FACT_SEARCH = '/production/facts_search/search?'
NODE_SEARCH = '/production/facts/'

class DictProblem(Exception):
    """
    There is a problem with your dict.
    """
    pass

class TargetProblem(Exception):
    pass

class HTTPCodeProblem(Exception):
    pass

class CurlActions(object):

    first_query_results_yaml = None
    targets = []
    second_query = {}

    def __init__(self, target=None, fact_search=True, **kwargs):
        """
        facts is a parsed hash of facts, that are by default stored in a classvar 
        in the UserInput class. 

        target is optional, and used when fact_search = False,
        This implementaion is not great- it will switch the URL global 
        from FACT_SEARCH to NODE_SEARCH, and do some other things. This is used
        when we have to do a 2nd lookup, to find an alternative factoutput (-o)
        """
        self.target         = target
        self.facts          = kwargs.get('facts', ui.facts)
        self.puppetmaster   = kwargs.get('puppetmaster', ui.data['puppetmaster'])
        self.ssl_cert       = kwargs.get('ssl_cert', ui.data['ssl_cert'])
        self.ssl_key        = kwargs.get('ssl_key', ui.data['ssl_key'])
        self.output_fact    = kwargs.get('output_fact', ui.data['output_fact'])
        self.debug          = kwargs.get('debug', ui.data['debug'])

        if fact_search:
            if self.target is not None:
                raise TargetProblem('fact_search is true, but I received a target, this should not happen')
            self.url = self._url_prep(self.puppetmaster, FACT_SEARCH, self._query_prep(self._fact_prep(self.facts)))
            if self.debug: print "built a query URL: " + self.url
        else:
            if self.target is None:
                raise TargetProblem('fact_search is false, but I did not receive a target, this should not happen')
            self.url = self._url_prep(self.puppetmaster, NODE_SEARCH, self.target)
            if self.debug: print "built a query URL: " + self.url
        
        self.response_buffer = StringIO.StringIO()

        self.c = pycurl.Curl()
        self.c.setopt(pycurl.URL, self.url)
        self.c.setopt(pycurl.WRITEFUNCTION, self.response_buffer.write)
        #self.c.setopt(pycurl.FOLLOWLOCATION, True)
        #self.c.setopt(pycurl.MAXREDIRS, 5)
        self.c.setopt(pycurl.HTTPHEADER, ["Accept: yaml"])
        self.c.setopt(pycurl.SSLCERT, self.ssl_cert)
        self.c.setopt(pycurl.SSLKEY, self.ssl_key)
        self.c.setopt(pycurl.SSL_VERIFYPEER, False)
        self.c.setopt(pycurl.SSL_VERIFYHOST, False)

    def _fact_prep(self, d, append_string='facts.'):
        """
        Recursive function that I found on stackoverflow to append facts. to 
        every key in the dict
        """
        if type(d) is dict:
            return dict([(append_string + k, self._fact_prep(v)) for k, v in d.items()])
        else:
            return d
    
    def _query_prep(self, query_dict):
        """
        Setup standard http-style post-back &query=foo
        """
        if self.debug:
            print "building a query string for %s" % str(query_dict)
        return urllib.urlencode(query_dict)

    def _url_prep(self, puppetmaster, url_path, query=None):
        """
        Will build a complete URL, containing hostname, query path, and query
        """
        if query is None:
            query = self.facts
        if self.debug: 
            print "running url prep for: " + str(query)
        return puppetmaster + url_path + query

    def run(self):
        """
        Sends the built request to the API, updates a classvar with the 
        output from the req
        """
        if self.debug: print "connecting to: " + self.url
        self.c.perform()

        if self.check_http_code():
            CurlActions.first_query_results_yaml = self.response_buffer.getvalue()
            return True
        else:
            raise HTTPCodeProblem('Error connecting to the Puppet inventory API')

    def check_http_code(self):
        """
        check the http code to make sure the query was successful
        """
        self.http_code = self.c.getinfo(pycurl.HTTP_CODE)
        if self.http_code != 200:
            if self.debug: print "Problems connecting to to API, HTTP Code was: %s" % (self.http_code)
            return False
        else:
            if self.debug: print "Successfully connected to API"
            return True

    def return_yaml(self):
        if self.debug: print "returning yaml"
        return CurlActions.first_query_results_yaml

