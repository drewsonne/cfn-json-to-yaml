import yaml

from cfnjsontoyaml.yamlobject.cfnfunction import CfnFunction


class Ref(CfnFunction):
    yaml_tag = u'!Ref'

    def __to_sub_string(self):
        return self.value

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
