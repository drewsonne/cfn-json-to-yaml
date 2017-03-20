import yaml


class Select(yaml.YAMLObject):
    yaml_tag = u'!Select'

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return '{tag}({value})'.format(tag=self.__class__.__name__, value=self.value)

    @staticmethod
    def representer(dumper, data):
        return dumper.represent_sequence(u'!Select', data.value, flow_style='plain')

    @staticmethod
    def constructor(loader, node):
        value = loader.construct_scalar(node)
        return Select(value)

if __name__ == 'cfnjsontoyaml.yamlobject.select':
    yaml.add_representer(Select, Select.representer)
    yaml.add_constructor(u'!Select', Select.constructor)
