from nose.tools import *
from  query_tool.user_input import UserInput

MOCK_DATA1 = {
    'ssl_key': '/var/lib/puppet/ssl/private_keys/query_tool.pem', 
    'ssl_cert': '/var/lib/puppet/ssl/certs/query_tool.pem', 
    'puppetmaster': 'https://127.0.0.1:8140', 
    'yaml': False, 
    'debug': True, 
    'fact': [['server_type', 'webapp']], 
    'output_fact': 'fqdn'
}

MOCK_DATA2 = {
    'ssl_key': '/var/lib/puppet/ssl/private_keys/query_tool.pem', 
    'ssl_cert': '/var/lib/puppet/ssl/certs/query_tool.pem', 
    'puppetmaster': 'https://127.0.0.1:8140', 
    'yaml': False, 
    'debug': True, 
    'fact': [['server_type', 'webapp'], ['ec2_instance_type', 'm1.large']], 
    'output_fact': 'fqdn'
}

MOCK_DATA_OUTPUT = {
    'ssl_key': '/var/lib/puppet/ssl/private_keys/query_tool.pem', 
    'ssl_cert': '/var/lib/puppet/ssl/certs/query_tool.pem', 
    'puppetmaster': 'https://127.0.0.1:8140', 
    'yaml': False, 
    'debug': True, 
    'fact': [['server_type', 'webapp']], 
    'output_fact': 'hostname'
}

def test_test():
    assert 1

def debug_test():
    ui = UserInput(['--fact', 'server_type', 'webapp', '--debug'])
    assert_equal(ui.data['debug'], True)

def debug_test2():
    ui = UserInput(['--fact', 'server_type', 'webapp', '--debug'])
    data = ui.get_args_as_dict()
    assert_equal(data, MOCK_DATA1)

def two_facts_test():
    ui = UserInput(['--fact', 'server_type', 'webapp', '--debug', '--fact', 'ec2_instance_type', 'm1.large'])
    data = ui.get_args_as_dict()
    assert_equal(data, MOCK_DATA2)

def output_test():
    ui = UserInput(['--fact', 'server_type', 'webapp', '--debug', '-o', 'hostname'])
    data = ui.get_args_as_dict()
    assert_equal(data, MOCK_DATA_OUTPUT)
