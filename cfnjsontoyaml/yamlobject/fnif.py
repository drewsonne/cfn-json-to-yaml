import yaml

from cfnjsontoyaml.yamlobject.cfnfunction import CfnFunction


class If(CfnFunction):
    yaml_tag = u'!If'

    @staticmethod
    def representer(dumper, data):
        return dumper.represent_sequence(u'!If', data.value, flow_style=True)

    @staticmethod
    def constructor(loader, node):
        value = loader.construct_scalar(node)
        return If(value)

if __name__ == 'cfnjsontoyaml.yamlobject.fnif':
    yaml.add_representer(If, If.representer)
    yaml.add_constructor(u'!If', If.constructor)
