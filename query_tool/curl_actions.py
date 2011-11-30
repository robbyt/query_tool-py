import pycurl
import StringIO
import yaml
import urllib

class DictProblem(Exception):
    """
    There is a problem with your dict.
    """
    pass

class CurlActions(object):
    def __init__(self, facts, **kwargs):
        self.facts          = facts
        self.puppetmaster   = kwargs['puppetmaster']
        self.ssl_cert       = kwargs['ssl_cert']
        self.ssl_key        = kwargs['ssl_key']
        self.yaml           = kwargs['yaml']
        self.output_fact    = kwargs['output_fact']
        self.debug          = kwargs['debug']
        
        self.response_buffer = StringIO.StringIO()
        self.url = self._url_prep(self.puppetmaster, self._fact_prep(self.facts))

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

    def _fact_prep(self, d):
        if type(d) is dict:
            return dict([('facts.' + k, self._fact_prep(v)) for k, v in d.items()])
        else:
            return d
        
    def _url_prep(self, puppetmaster, facts):
        return puppetmaster + urllib.urlencode(facts)

    def run(self):
        if self.debug: print "connecting to: " + self.url
        self.c.perform()

    def return_yaml(self):
        return self.response_buffer.getvalue()

    def return_text(self):
        self.y = yaml.load(self.response_buffer.getvalue())
        return '\n'.join(self.y)

        #for line in self.y:
        #    print line
