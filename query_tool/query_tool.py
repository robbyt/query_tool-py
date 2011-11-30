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

    if data['yaml']:
        print action.return_yaml()
    else:
        print action.return_text()
