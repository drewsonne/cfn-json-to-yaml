import yaml

from cfnjsontoyaml.yamlobject.cfnfunction import CfnFunction


class And(CfnFunction):
    yaml_tag = u'!And'

    @staticmethod
    def representer(dumper, data):
        return dumper.represent_sequence(u'!And', data.value, flow_style=True)

    @staticmethod
    def constructor(loader, node):
        value = loader.construct_scalar(node)
        return And(value)

if __name__ == 'cfnjsontoyaml.yamlobject.fnand':
    yaml.add_representer(And, And.representer)
    yaml.add_constructor(u'!And', And.constructor)
