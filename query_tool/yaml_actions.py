from yaml import load, add_constructor
#from yaml import dump
from user_input import UserInput as ui

#try:
#    from yaml import CLoader as Loader, CDumper as Dumper
#except ImportError:
#    from yaml import Loader, Dumper

class Tbd(Exception):
    pass

class YamlActions(object):

    def __init__(self):
        self._yaml_hack()

    def _yaml_builder(self, loader, node):
        if ui.debug: print "Building some yaml"
        return loader.construct_mapping(node)['values']

    def _yaml_hack(self):
        if ui.debug: print "Adding the yaml hack"
        add_constructor(u'!ruby/object:Puppet::Node::Facts', self._yaml_builder)

    def to_text(self, yaml_string):
        if ui.debug: print "returning text"
        t = load(yaml_string)
        return '\n'.join(t)

    def to_list(self, yaml_string):
        if ui.debug: print "returning a python list object"
        return load(yaml_string)

    def to_dict(self, yaml_string):
        raise Tbd
