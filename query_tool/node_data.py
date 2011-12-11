from user_input import UserInput as ui
from yaml_actions import YamlActions

class NodeData(object):
    targets = []
    facts = {}

    def __init__(self):
        self.debug = ui.data['debug']
        self.yaml = YamlActions()

    def store_targets(self, targets):
        if self.debug: print "Storing targets/FQDNs: %s" % (", ".join(targets))
        NodeData.targets = self.yaml.to_dict(targets)
    
    def store_facts(self, target, facts_dict):
        if self.debug: print "Storing facts hash for: %s" % (target)
        NodeData.facts[target] =  self.yaml.to_dict(facts_dict)

