import yaml


class Ref(yaml.YAMLObject):
    yaml_tag = u'!Ref'

    def __init__(self, value):
        self.value = value

    def __to_sub_string(self):
        return self.value

    def __repr__(self):
        return '{tag}({value})'.format(tag=self.__class__.__name__, value=self.value)

    @staticmethod
    def representer(dumper, data):
        return dumper.represent_scalar(u'!Ref', data.value, style='plain')

    @staticmethod
    def constructor(loader, node):
        value = loader.construct_scalar(node)
        return Ref(value)

if __name__ == 'cfnjsontoyaml.yamlobject.ref':
    yaml.add_representer(Ref, Ref.representer)
    yaml.add_constructor(u'!Ref', Ref.constructor)
