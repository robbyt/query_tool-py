#!/usr/bin/env python
import sys
from user_input import UserInput
from curl_actions import CurlActions
from output_actions import OutputActions

class Tbd(Exception):
    pass

if __name__ == '__main__':
    # parse the args
    ui = UserInput(sys.argv[1:])

    # throw that dict at the curlactions class to get our data
    action = CurlActions()

    # perform the query
    action.run()

    # throw the output from that query into the output parser
    output = OutputActions(action.return_yaml())

    # if we're just going to output fqdn, just show the list of servers
    if output.default_output():
        print output
    else:
    # otherwise, we need to run a few more queries to return the requested output type
        raise Tbd('not done yet')

    """
    ### end ###
    # if the output format is default, just output the FQDNs
        
        if ui.data['yaml']:
            print action.return_yaml()
        else:
            print y.to_text(action.return_yaml())

    # otherwise, we have to do some more work
    else:
        search_results = {}
        for t in y.to_list(action.return_yaml()):
            node_search = CurlActions(target=t, fact_search=False, **data)
            node_search.run()
            search_results[t] = y.to_text(node_search.return_yaml())
            if data['debug']: print 'Added a new element to search_results: %s' % (search_results[t])

        if data['yaml']:
            print 'not implemented.'
        else:
            for i in search_results.iteritems():
                print i
        
    """ 
