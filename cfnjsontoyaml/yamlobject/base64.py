import yaml

from cfnjsontoyaml.yamlobject.cfnfunction import CfnFunction
from cfnjsontoyaml.yamlobject.join import Join


class Base64(CfnFunction):
    yaml_tag = u'!Base64'

    @staticmethod
    def representer(dumper, data):
        if type(data.value) in [str, unicode, Join]:
            return dumper.represent_scalar(u'!Base64', data.value, style='double-quoted')
        else:
            return dumper.represent_sequence(u'!Base64', data.value, flow_style=True)

    @staticmethod
    def constructor(loader, node):
        value = loader.construct_scalar(node)
        return Base64(value)

if __name__ == 'cfnjsontoyaml.yamlobject.base64':
    yaml.add_representer(Base64, Base64.representer)
    yaml.add_constructor(u'!Base64', Base64.constructor)
