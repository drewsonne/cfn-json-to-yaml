import yaml


class GetAtt(yaml.YAMLObject):
    yaml_tag = u'!GetAtt'

    def __init__(self, attribute):
        self.value = "{0}.{1}".format(*attribute)

    def __repr__(self):
        return '{tag}({value})'.format(tag=self.__class__.__name__, value=self.value)

    @staticmethod
    def representer(dumper, data):
        return dumper.represent_scalar(u'!GetAtt', data.value, style='double-quoted')

    @staticmethod
    def constructor(loader, node):
        value = loader.construct_scalar(node)
        return GetAtt(value)


if __name__ == 'cfnjsontoyaml.yamlobject.getatt':
    yaml.add_representer(GetAtt, GetAtt.representer)
    yaml.add_constructor(u'!GetAtt', GetAtt.constructor)
