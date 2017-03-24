import yaml

from cfnjsontoyaml.yamlobject.cfnfunction import CfnFunction


class Or(CfnFunction):
    yaml_tag = u'!Or'

    @staticmethod
    def representer(dumper, data):
        return dumper.represent_sequence(u'!Or', data.value, flow_style=True)

    @staticmethod
    def constructor(loader, node):
        value = loader.construct_scalar(node)
        return Or(value)

if __name__ == 'cfnjsontoyaml.yamlobject.fnor':
    yaml.add_representer(Or, Or.representer)
    yaml.add_constructor(u'!Or', Or.constructor)
