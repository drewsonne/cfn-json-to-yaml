import yaml


class If(yaml.YAMLObject):
    yaml_tag = u'!If'

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return '{tag}({value})'.format(tag=self.__class__.__name__, value=self.value)

    @staticmethod
    def representer(dumper, data):
        return dumper.represent_sequence(u'!If', data.value, flow_style=True)

    @staticmethod
    def constructor(loader, node):
        value = loader.construct_scalar(node)
        return If(value)

if __name__ == 'cfnjsontoyaml.yamlobject.fnif':
    yaml.add_representer(If, If.representer)
    yaml.add_constructor(u'!If', If.constructor)
