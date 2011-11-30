import pycurl
import StringIO
import yaml
import urllib

class CurlActions(object):
    __init__(self, facts, **kwargs):
        self.facts          = facts
        self.puppetmaster   = kwargs['puppetmaster']
        self.cert           = kwargs['cert']
        self.key            = kwargs['key']
        self.yaml           = kwargs['yaml']
        self.output_fact    = kwargs['output_fact']
        self.url            = self.puppetmaster + urllib.urlencode(self.facts)
        

        self.response_buffer = StringIO.StringIO()

        self.c = pycurl.Curl()
        self.c.setopt(pycurl.URL, self.url)
        self.c.setopt(pycurl.WRITEFUNCTION, self.response_buffer.write)
        self.c.setopt(pycurl.FOLLOWLOCATION, True)
        self.c.setopt(pycurl.MAXREDIRS, 5)
        self.c.setopt(pycurl.HTTPHEADER, ["Accept: yaml"])
#        self.c.setopt(pycurl.CAPATH, self.ca)
        self.c.setopt(pycurl.SSLCERT, self.cert)
        self.c.setopt(pycurl.SSLKEY, self.key)
        self.c.setopt(pycurl.SSL_VERIFYPEER, False)
        self.c.setopt(pycurl.SSL_VERIFYHOST, False)

    def run(self):
        self.c.perform()

    def return_yaml(self):
        return self.response_buffer.getvalue()

    def return_text(self):
        self.y = yaml.load(self.response_buffer.getvalue())
        for line in y:
            print line
