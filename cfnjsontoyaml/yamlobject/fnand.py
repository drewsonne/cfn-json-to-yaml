import yaml


class And(yaml.YAMLObject):
    yaml_tag = u'!And'

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return '{tag}({value})'.format(tag=self.__class__.__name__, value=self.value)

    @staticmethod
    def representer(dumper, data):
        return dumper.represent_sequence(u'!And', data.value, flow_style=True)

    @staticmethod
    def constructor(loader, node):
        value = loader.construct_scalar(node)
        return And(value)

if __name__ == 'cfnjsontoyaml.yamlobject.fnand':
    yaml.add_representer(And, And.representer)
    yaml.add_constructor(u'!And', And.constructor)
