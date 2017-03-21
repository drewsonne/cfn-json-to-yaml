import yaml

from cfnjsontoyaml.mixins.type_checker import TypeChecker
from cfnjsontoyaml.yamlobject.cfnfunction import CfnFunction


class ImportValue(CfnFunction, TypeChecker):
    yaml_tag = u'!ImportValue'

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
