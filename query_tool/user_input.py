import sys
import argparse
import os

class UserInput(object):
    usage = "Please read --help"

    def __init__(self, args):
        '''
        sets up the user input system. When setting up this 
        class, pass sys.argv[1:] into the class, otherwise for testing
        pass in a dict of simulated arguments
        '''
        
        # setup the parser
        self.parser = argparse.ArgumentParser(description='query_tool')

        # prep some variables
        self.args = args
        self.htext = {
            'fact':         "The fact:data that you want to search for, can be used multiple times to filter for multiple facts. Usage Example: --fact kernel Linux --fact ec2_size m1.small",
            'puppetmaster': 'The PuppetMaster REST address to query against. Must be formatted like this: https://127.0.0.1:8140/',
            'ssl_cert':         'The SSL cert to use for authentication',
            'ssl_key':          'The SSL key to use for authentication',
            'yaml':         'Output the results in raw yaml',
            'output_fact':  'What fact do you want to find out from these servers'
        }

        #run the arg parser methods
        self._setup_args()

    def _setup_args(self):
        '''operands, or server/cluster to perform an operation on'''
        # elb_name
        self.parser.add_argument(
            "-f", "--fact",
            action='append',
            dest="fact",
            help=self.htext['fact'],
            required=True,
            nargs=2, 
            metavar=('factname', 'factvalue')
        )

        self.parser.add_argument(
            "-p", "--puppetmaster",
            dest="puppetmaster",
            help=self.htext['puppetmaster'],
            default='https://127.0.0.1:8140/'
        )

        self.parser.add_argument(
            "-c", "--cert",
            dest="ssl_cert",
            help=self.htext['ssl_cert'],
            default='/var/lib/puppet/ssl/certs/query_tool.pem'
        )

        self.parser.add_argument(
            "-k", "--key",
            dest="ssl_key",
            help=self.htext['ssl_key'],
            default='/var/lib/puppet/ssl/private_keys/query_tool.pem'
        )

        self.parser.add_argument(
            "--yaml",
            action="store_true",
            dest="yaml",
            help=self.htext['yaml'],
            default=False
        )

        self.parser.add_argument(
            "--output_fact",
            dest="output_fact",
            help=self.htext['output_fact'],
            default='fqdn'
        )

        ## other options
        self.parser.add_argument("--debug", action="store_true", dest="debug", default=False)

    def _parse_args(self):
        return self.parser.parse_args(self.args)
    
    def get_args_as_dict(self):
        d = vars(self._parse_args())
        if self.debug_enabled():
            print 'parsed args in dict:'
            for i in d.iteritems():
                print i
        return d

    def get_facts_as_dict(self):
        d = self._parse_args()
        if self.debug_enabled(): print 'parsed facts: ' + str(d.fact)
        return dict(d.fact)

    def debug_enabled(self):
        res = self._parse_args()
        return res.debug


