import yaml

from cfnjsontoyaml.yamlobject.cfnfunction import CfnFunction


class GetAZs(CfnFunction):
    yaml_tag = u'!GetAZs'

    @staticmethod
    def representer(dumper, data):
        return dumper.represent_scalar(u'!GetAZs', data.value, style='double-quoted')

    @staticmethod
    def constructor(loader, node):
        value = loader.construct_scalar(node)
        return GetAZs(value)

if __name__ == 'cfnjsontoyaml.yamlobject.getazs':
    yaml.add_representer(GetAZs, GetAZs.representer)
    yaml.add_constructor(u'!GetAZs', GetAZs.constructor)
