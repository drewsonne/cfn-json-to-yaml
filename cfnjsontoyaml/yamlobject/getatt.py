import yaml

from cfnjsontoyaml.yamlobject.cfnfunction import CfnFunction


class GetAtt(CfnFunction):
    yaml_tag = u'!GetAtt'

    def __init__(self, attribute):
        super(GetAtt, self).__init__("{0}.{1}".format(*attribute))

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
