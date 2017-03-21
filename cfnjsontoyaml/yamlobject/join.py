import yaml

from cfnjsontoyaml.yamlobject.cfnfunction import CfnFunction


class Join(CfnFunction):
    yaml_tag = u'!Join'

    @staticmethod
    def representer(dumper, data):
        return dumper.represent_sequence(u'!Join', data.value, flow_style='double-quoted')

    @staticmethod
    def constructor(loader, node):
        value = loader.construct_scalar(node)
        return Join(value)

if __name__ == 'cfnjsontoyaml.yamlobject.join':
    yaml.add_representer(Join, Join.representer)
    yaml.add_constructor(u'!Join', Join.constructor)
