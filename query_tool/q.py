import pycurl
import StringIO
import yaml
import urllib

BASE_URL = 'https://127.0.0.1:8140/production/facts_search/search?'
PARAMS = {
    'facts.ec2_instance_type':'m1.small',
    'facts.server_type':'webapp',
}

#URL = 'https://127.0.0.1:8140/production/facts_search/search?facts.ec2_instance_type=m1.small&facts.server_type=webapp'
#URL = 'https://127.0.0.1:8140/'

URL = BASE_URL + urllib.urlencode(PARAMS)
print 'URL IS: ' + URL

CERT='/var/lib/puppet/ssl/certs/ec2_runner.pem'
KEY='/var/lib/puppet/ssl/private_keys/ec2_runner.pem'
CA='/var/lib/puppet/ssl/ca/ca_crt.pem'

response_buffer = StringIO.StringIO()

c = pycurl.Curl()
c.setopt(pycurl.URL, URL)
c.setopt(pycurl.WRITEFUNCTION, response_buffer.write)
c.setopt(pycurl.FOLLOWLOCATION, 1)
c.setopt(pycurl.MAXREDIRS, 5)
c.setopt(pycurl.HTTPHEADER, ["Accept: yaml"])
c.setopt(pycurl.CAPATH, CA)
c.setopt(pycurl.SSLCERT, CERT)
c.setopt(pycurl.SSLKEY, KEY)
c.setopt(pycurl.SSL_VERIFYPEER, False)
c.setopt(pycurl.SSL_VERIFYHOST, False)

c.perform()

y = yaml.load(response_buffer.getvalue())

print response_buffer.getvalue()

for line in y:
    print line

if 
