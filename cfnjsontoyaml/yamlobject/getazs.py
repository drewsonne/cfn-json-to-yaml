import yaml


class GetAZs(yaml.YAMLObject):
    yaml_tag = u'!GetAZs'

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return '{tag}({value})'.format(tag=self.__class__.__name__, value=self.value)

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
