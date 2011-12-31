#!/usr/bin/env python
import sys
from user_input import UserInput
from curl_actions import NodeSearch
from output_actions import OutputActions

import eventlet

if __name__ == '__main__':
    eventlet.monkey_patch()

    # parse the args
    ui = UserInput(sys.argv[1:])

    # create an instance of the curl actions class
    action = NodeSearch()

    # perform the query
    action.run()

    # save the results to NodeData
    action.save()

    # create an instance to read NodeData and UserInput and output data 
    output = OutputActions()

    print output

