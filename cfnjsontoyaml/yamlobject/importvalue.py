import yaml

from cfnjsontoyaml.mixins.type_checker import TypeChecker


class ImportValue(yaml.YAMLObject, TypeChecker):
    yaml_tag = u'!ImportValue'

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return '{tag}({value})'.format(tag=self.__class__.__name__, value=self.value)

    @staticmethod
    def representer(dumper, data):
        return dumper.represent_scalar(u'!ImportValue', data.value, style='double-quote')

    @staticmethod
    def constructor(loader, node):
        value = loader.construct_scalar(node)
        return ImportValue(value)

if __name__ == 'cfnjsontoyaml.yamlobject.importvalue':
    yaml.add_representer(ImportValue, ImportValue.representer)
    yaml.add_constructor(u'!ImportValue', ImportValue.constructor)
