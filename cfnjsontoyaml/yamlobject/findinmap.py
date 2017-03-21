import yaml

from cfnjsontoyaml.yamlobject.cfnfunction import CfnFunction


class FindInMap(CfnFunction):
    yaml_tag = u'!FindInMap'

    @staticmethod
    def representer(dumper, data):
        return dumper.represent_sequence(u'!FindInMap', data.value, flow_style=True)

    @staticmethod
    def constructor(loader, node):
        value = loader.construct_scalar(node)
        return FindInMap(value)

if __name__ == 'cfnjsontoyaml.yamlobject.findinmap':
    yaml.add_representer(FindInMap, FindInMap.representer)
    yaml.add_constructor(u'!FindInMap', FindInMap.constructor)
