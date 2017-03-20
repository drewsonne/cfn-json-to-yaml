from cfnjsontoyaml.mixins.type_checker import TypeChecker
from cfnjsontoyaml.yamlobject.importvalue import ImportValue
from cfnjsontoyaml.yamlobject.join import Join
from cfnjsontoyaml.yamlobject.ref import Ref
from cfnjsontoyaml.yamlobject.sub import Sub


class NodeParser(object):
    PARSER_OPTIONS = {
        'join_to_sub': False,
        'use_tag': True
    }

    def __init__(self, node, **options):

        # Set option defaults
        self.options = self.PARSER_OPTIONS.copy()
        self.options.update(options)

        if type(node) == dict:
            self._nodes = map(lambda node_pair: Node(*node_pair, parser=self, parent=None), node.items())
            self._node_type = dict

    def parse(self):

        for node in self._nodes:
            node.convert(use_tag=self.options['use_tag'])

        return dict(
            map(
                lambda node: node.to_dict(),
                self._nodes
            )
        )


class Node(TypeChecker):
    FUNCTION_MAPPING = {
        'Ref': Ref,
        # 'Fn::Base64',
        # 'Fn::FindInMap',
        # 'Fn::GetAtt',
        # 'Fn::GetAZs',
        'Fn::ImportValue': ImportValue,
        'Fn::Join': Join,
        # 'Fn::Select',
        'Fn::Sub': Sub,
        # 'Fn::And',
        # 'Fn::Equals',
        # 'Fn::If',
        # 'Fn::Not',
        # 'Fn::Or'
    }

    def __init__(self, key, value, parser, parent):
        self._key = key
        self._value = value
        self._raw_value = value
        self._parser = parser
        self.parent = parent

    def to_dict(self):
        return (
            self._key,
            self._value
        )

    def _get_function_node(self, value):
        return self.FUNCTION_MAPPING[self._get_function_key(value)]

    def convert(self, use_tag=True):
        if self._is_function(self._value):
            # If we're converting joins to subs
            if self._parser.options['join_to_sub'] and (self._get_function_key(self._value) == 'Fn::Join'):
                function__node_class = self.FUNCTION_MAPPING['Fn::Sub']
            else:
                function__node_class = self._get_function_node(self._value)

            _parser_options = self._parser.options.copy()
            _parser_options['parser_class'] = self._parser.__class__

            self._value = function__node_class(self._value, **_parser_options)
            self._value
        else:
            print 'not_function'
        return self
