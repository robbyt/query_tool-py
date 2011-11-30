#!/usr/bin/env python
import sys
from user_input import UserInput
from curl_actions import CurlActions

if __name__ == '__main__':
    # parse the args
    ui = UserInput(sys.argv[1:])

    # collect the parsed args into a dict
    data = ui.get_args_as_dict()

    # throw that dict at the curlactions class to get our data
    action = CurlActions(facts = ui.get_facts_as_dict(), **data)
    action.run()

    # if the output format is default, just output the FQDNs
    if data['output_fact'] == 'fqdn':
        if data['debug']: print 'output_fact is set to "%s" so we can return the current data' % (data['output_fact'])
        
        if data['yaml']:
            print action.return_yaml()
        else:
            print action.return_text()

    # otherwise, we have to do some more work
    else:
        if data['debug']: print 'output_fact is set to "%s" so we have to run some more queries' % (data['output_fact'])
        pass
        
        
