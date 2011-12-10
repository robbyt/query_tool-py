import sys
import argparse
import os

class UserInput(object):
    usage = "Please read --help"
    data = None
    facts = None
#    facts = {}
#    debug = False

    def __init__(self, args):
        '''
        sets up the user input system. When setting up this 
        class, pass sys.argv[1:] into the class, otherwise for testing
        pass in a dict of simulated arguments.

        When a class object is created, and passed a list of the unparsed 
        args, it will auto-parse them into dicts, stored as Class Variables
        data, facts.
        '''
        
        # setup the parser
        self.parser = argparse.ArgumentParser(description='query_tool')

        # prep some variables
        self.args = args
        self.htext = {
            'fact':         "The fact:data that you want to search for, can be used multiple times to filter for multiple facts. Usage Example: --fact kernel Linux --fact ec2_size m1.small",
            'puppetmaster': 'The PuppetMaster REST address to query against. Must be formatted like this: https://127.0.0.1:8140/',
            'ssl_cert':     'The SSL cert to use for authentication',
            'ssl_key':      'The SSL key to use for authentication',
            'yaml':         'Output the results in raw yaml',
            'output_fact':  'What fact do you want to find out from these servers'
        }

        # run the arg parser methods
        self._setup_args()

        # create a class variable with parsed args
        self._parse_args()

        # and store the results as class variables
        UserInput.data = self.get_args_as_dict()
        UserInput.facts = self.get_facts_as_dict()

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
            default='https://127.0.0.1:8140'
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
            "-o", "--output_fact",
            dest="output_fact",
            help=self.htext['output_fact'],
            default='fqdn'
        )

        ## other options
        self.parser.add_argument("--debug", action="store_true", dest="debug", default=False)

    def _parse_args(self):
        """
        Parses the args that were passed into sys.argv, then creates a dict
        containing the various key/values after being parsed
        """
        UserInput.data = vars(self.parser.parse_args(self.args))
        UserInput.facts = vars(self.parser.parse_args(self.args))['fact']
        return UserInput.data
    
    def _get_args_as_dict(self):
        if UserInput.data['debug']:
            print 'parsed args in dict:'
            for i in UserInput.data.iteritems():
                print i
        return UserInput.data

    def _get_facts_as_dict(self):
        if UserInput.data['debug']:
            print 'parsed facts: ' + str(UserInput.data['fact'])
        return dict(UserInput.data['fact'])

    #def debug(self):
    #    UserInput.debug = self.parsed_args['debug']
    #    return UserInput.data['debug']

#    def debug_say(self, msg):
#        if self.debug():
#            print msg


