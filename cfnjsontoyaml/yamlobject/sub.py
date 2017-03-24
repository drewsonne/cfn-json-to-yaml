import yaml

from cfnjsontoyaml.parser.subbuilder import SubBuilder
from cfnjsontoyaml.yamlobject.cfnfunction import CfnFunction


class Sub(CfnFunction):
    yaml_tag = u'!Sub'

    def __init__(self, value, use_literal=False):
        pattern, substitutions = value
        if substitutions is None:
            value = pattern
        else:
            value = value
        super(Sub, self).__init__(value)

        self.use_literal = False if (len(value) < 30) else use_literal

    @property
    def is_sequence(self):
        return type(self.value) in [list, tuple]

    @staticmethod
    def representer(dumper, data):
        if data.is_sequence:

            use_literal = "\n" in data.value[0]
            if use_literal:
                pattern = Literal(data.value[0])
            else:
                pattern = data.value[0]

            substitutions = data.value[1]

            return dumper.represent_sequence(u'!Sub', [pattern, substitutions], flow_style=False)
        else:
            return dumper.represent_scalar(u'!Sub', data.value, style=('|' if data.use_literal else '"'))

    @staticmethod
    def constructor(loader, node):
        value = loader.construct_scalar(node)
        return Sub(value)


class Literal(str): pass


def literal_presenter(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')


if __name__ == 'cfnjsontoyaml.yamlobject.sub':
    yaml.add_representer(Sub, Sub.representer)
    yaml.add_constructor(u'!Ref', Sub.constructor)
    yaml.add_representer(Literal, literal_presenter)
