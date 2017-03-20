import yaml


class Not(yaml.YAMLObject):
    yaml_tag = u'!Not'

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return '{tag}({value})'.format(tag=self.__class__.__name__, value=self.value)

    @staticmethod
    def representer(dumper, data):
        return dumper.represent_sequence(u'!Not', data.value, flow_style=True)

    @staticmethod
    def constructor(loader, node):
        value = loader.construct_scalar(node)
        return Not(value)

if __name__ == 'cfnjsontoyaml.yamlobject.not':
    yaml.add_representer(Not, Not.representer)
    yaml.add_constructor(u'!Or', Not.constructor)
