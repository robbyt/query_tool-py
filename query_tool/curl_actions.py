import pycurl
import StringIO
from yaml import load, dump, add_constructor
import urllib

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


FACT_SEARCH = '/production/facts_search/search?'
NODE_SEARCH = '/production/fact/'

class DictProblem(Exception):
    """
    There is a problem with your dict.
    """
    pass

class TargetProblem(Exception):
    pass

class HTTPCodeProblem(Exception):
    pass

def yaml_hack():
    def yaml_builder(loader, node):
        return loader.construct_mapping(node)['values']
    add_constructor(u'!ruby/object:Puppet::Node::Facts', yaml_builder)


class CurlActions(object):
    def __init__(self, facts=None, target=None, fact_search=True,**kwargs):
        self.facts          = facts
        self.target         = target
        self.puppetmaster   = kwargs['puppetmaster']
        self.ssl_cert       = kwargs['ssl_cert']
        self.ssl_key        = kwargs['ssl_key']
        self.yaml           = kwargs['yaml']
        self.output_fact    = kwargs['output_fact']
        self.debug          = kwargs['debug']

        if fact_search:
            if self.target is not None:
                raise TargetProblem('fact_search is true, but I received a target, this should not happen')
            self.url = self._url_prep(self.puppetmaster, FACT_SEARCH, self._query_prep(self._fact_prep(self.facts)))
            if self.debug: print "built a query URL: " + self.url
        else:
            if self.target is None:
                raise TargetProblem('fact_search is false, but I did not receive a target, this should not happen')
            yaml_hack()
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
        if self.debug: print "connecting to: " + self.url
        self.c.perform()

        # check the http code to make sure the query was successful
        self.http_code = self.c.getinfo(pycurl.HTTP_CODE)
        if self.http_code != 200:
            raise HTTPCodeProblem('Error connecting to the Puppet inventory API, received http code: %s' % (self.http_code))
        else:
            if self.debug: print "Successfully connected to API"
            return True

    def return_yaml(self):
        if self.debug: print "returning yaml"
        return self.response_buffer.getvalue()

    def return_text(self):
        if self.debug: print "returning text"
        self.y = load(self.response_buffer.getvalue(), Loader=Loader)
        return '\n'.join(self.y)

    def return_list(self):
        if self.debug: print "returning a python list object"
        return load(self.response_buffer.getvalue())

