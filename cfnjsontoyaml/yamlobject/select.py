import yaml

from cfnjsontoyaml.yamlobject.cfnfunction import CfnFunction


class Select(CfnFunction):
    yaml_tag = u'!Select'

    @staticmethod
    def representer(dumper, data):
        return dumper.represent_sequence(u'!Select', data.value, flow_style='plain')

    @staticmethod
    def constructor(loader, node):
        value = loader.construct_scalar(node)
        return Select(value)

if __name__ == 'cfnjsontoyaml.yamlobject.select':
    yaml.add_representer(Select, Select.representer)
    yaml.add_constructor(u'!Select', Select.constructor)
