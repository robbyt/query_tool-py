from yaml import load, add_constructor
#from yaml import dump
from user_input import UserInput as ui

class YamlActions(object):

    def __init__(self):
        self._yaml_hack()

    def _yaml_builder(self, loader, node):
        if ui.debug: print "Building some yaml"
        return loader.construct_mapping(node)['values']

    def _yaml_hack(self):
        if ui.debug: print "Adding the yaml custom tag hack"
        add_constructor(u'!ruby/object:Puppet::Node::Facts', self._yaml_builder)

    def to_text(self, yaml_string):
        if ui.debug: print "returning text from yaml"
        t = load(yaml_string)
        return '\n'.join(t)

    def to_dict(self, yaml_string):
        if ui.debug: print "returning a python dict object from yaml"
        return load(yaml_string)

