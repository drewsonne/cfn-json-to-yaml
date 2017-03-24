import yaml

from cfnjsontoyaml.yamlobject.cfnfunction import CfnFunction


class Not(CfnFunction):
    yaml_tag = u'!Not'

    @staticmethod
    def representer(dumper, data):
        return dumper.represent_sequence(u'!Not', data.value, flow_style=True)

    @staticmethod
    def constructor(loader, node):
        value = loader.construct_scalar(node)
        return Not(value)

if __name__ == 'cfnjsontoyaml.yamlobject.fnnot':
    yaml.add_representer(Not, Not.representer)
    yaml.add_constructor(u'!Not', Not.constructor)
