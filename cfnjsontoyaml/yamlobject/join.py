import yaml

class Join(yaml.YAMLObject):
    yaml_tag = u'!Join'

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return '{tag}({value})'.format(tag=self.__class__.__name__, value=self.value)

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
