from cfnjsontoyaml.parser.ref import RefParser


class FunctionParser(object):
    def __init__(self, node):
        self._node = node

    @classmethod
    def factory(cls, _node):
        function_name = cls._get_function_key(_node)
        return {
            'Ref': RefParser
        }[function_name](_node)

    @staticmethod
    def _get_function_key(node):
        return node.keys()[0]
