import yaml

from cfnjsontoyaml.yamlobject.cfnfunction import CfnFunction


class Equals(CfnFunction):
    yaml_tag = u'!Equals'

    @staticmethod
    def representer(dumper, data):
        return dumper.represent_sequence(u'!Equals', data.value, flow_style=True)

    @staticmethod
    def constructor(loader, node):
        value = loader.construct_scalar(node)
        return Equals(value)

if __name__ == 'cfnjsontoyaml.yamlobject.equals':
    yaml.add_representer(Equals, Equals.representer)
    yaml.add_constructor(u'!Equals', Equals.constructor)
