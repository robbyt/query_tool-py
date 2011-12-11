from yaml_actions import YamlActions
from curl_actions import FactSearch
from user_input import UserInput as ui

class Tbd(Exception):
    pass

class OutputActions(object):
    def __init__(self, yaml_from_first_query,**kwargs):
        self.output_fact = kwargs.get('output_fact', ui.data['output_fact'])
        self.yaml_enabled = kwargs.get('yaml', ui.data['yaml'])
        self.yaml_from_first_query = yaml_from_first_query

        self.y = YamlActions()


    def __str__(self):
        return self.default_output()

    def default_output(self):
        """
        This method is used if we do not have to run a second set of queries 
        against the API to find another fact (other than FQDN).

        The first query to the API will return a list of FQDNs, if we require
        information other than just the FQDN name, we need to run a second 
        set of queries against the API for each of those hostnames. Annoying.
        """
        if self._output_type_is_fqdn:
            return self.y.to_text(self.yaml_from_first_query)
        else:
            raise Tbd
       #     return self.y

    def _target_to_fact_dict(self, target):
        """
        Feed me a target, and I'll return all facts about that target
        """
        facts = FactSearch(target=target)
        facts.run()
        return self.y.to_text(facts.return_yaml())

    def _output_type_is_fqdn(self):
        """
        check to see if the output type matches fqdn (the default)
        If it does match, we'll just return true. However, if it does not match
        That means we'll have to do some more work here
        """
        if ui.debug: print 'output_fact is set to "%s"' % (self.output_fact)
        if self.output_fact == 'fqdn':
            if ui.debug: print 'default output type found'
            return True
        else:
            if ui.debug: print 'non-default output type found'
            return False


    def _yaml_picker(self):
        """
        will output yaml, if yaml == True, otherwise will output text
        """
        if self.yaml_enabled:
            return self.output_yaml()
        else:
            return self.output_text()

