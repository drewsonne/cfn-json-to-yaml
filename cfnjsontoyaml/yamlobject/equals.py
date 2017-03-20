import yaml


class Equals(yaml.YAMLObject):
    yaml_tag = u'!Equals'

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return '{tag}({value})'.format(tag=self.__class__.__name__, value=self.value)

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
