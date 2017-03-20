import yaml


class Or(yaml.YAMLObject):
    yaml_tag = u'!Or'

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return '{tag}({value})'.format(tag=self.__class__.__name__, value=self.value)

    @staticmethod
    def representer(dumper, data):
        return dumper.represent_sequence(u'!Or', data.value, flow_style=True)

    @staticmethod
    def constructor(loader, node):
        value = loader.construct_scalar(node)
        return Or(value)

if __name__ == 'cfnjsontoyaml.yamlobject.or':
    yaml.add_representer(Or, Or.representer)
    yaml.add_constructor(u'!Or', Or.constructor)
