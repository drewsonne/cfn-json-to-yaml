import yaml


class FindInMap(yaml.YAMLObject):
    yaml_tag = u'!FindInMap'

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return '{tag}({value})'.format(tag=self.__class__.__name__, value=self.value)

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
