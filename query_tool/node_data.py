from user_input import UserInput as ui
from yaml_actions import YamlActions

class NodeData(object):
    targets = []
    facts = []

    def __init__(self):
        self.debug = ui.data['debug']
        self.yaml = YamlActions()

    def store_targets(self, targets):
        self.data = self.yaml.to_dict(targets)
        if self.debug: print "Storing targets/FQDNs: %s" % (self.data)
        NodeData.targets = self.data
    
    def store_facts(self, target, facts_dict):
        if self.debug: print "Storing facts hash for: %s" % (target)
        #NodeData.facts[target] =  self.yaml.to_dict(facts_dict)
        NodeData.facts.append(self.yaml.to_dict(facts_dict))

    def get_fact_from_facts(self, fact_to_find):
        """
        This is used to iterate the list of fact dicts, and pull out a single
        fact from the dictionaries within.
        """

        data = []
        for l in NodeData.facts:
            try:
                data.append(l[fact_to_find])
            except KeyError:
                pass

        return data

