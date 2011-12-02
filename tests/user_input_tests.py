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

def single_fact_test1():
    ui = UserInput(['--fact', 'server_type', 'webapp', '--debug'])
    data = ui.get_args_as_dict()
    data_class_var = ui.data
    facts = ui.get_facts_as_dict()
    facts_class_var = ui.get_facts_as_dict()
    assert_equal(data, MOCK_DATA1)
    assert_equal(data, data_class_var)
    assert_equal(facts, {'server_type': 'webapp'} )
    assert_equal(facts, facts_class_var)

def single_fact_test2():
    ui = UserInput(['--fact', 'server_type', 'webapp', '--debug'])
    data = ui.get_facts_as_dict()

def two_facts_test():
    ui = UserInput(['--fact', 'server_type', 'webapp', '--debug', '--fact', 'ec2_instance_type', 'm1.large'])
    data = ui.get_args_as_dict()
    facts = ui.get_facts_as_dict()
    assert_equal(data, MOCK_DATA2)
    assert_equal(facts, {'server_type': 'webapp', 'ec2_instance_type': 'm1.large'} )

def output_test():
    ui = UserInput(['--fact', 'server_type', 'webapp', '--debug', '-o', 'hostname'])
    data = ui.get_args_as_dict()
    assert_equal(data, MOCK_DATA_OUTPUT)
