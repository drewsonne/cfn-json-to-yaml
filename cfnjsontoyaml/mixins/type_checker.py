class TypeChecker(object):
    FUNCTIONS = [
        'Ref',
        'Fn::Base64',
        'Fn::FindInMap',
        'Fn::GetAtt',
        'Fn::GetAZs',
        'Fn::ImportValue',
        'Fn::Join',
        'Fn::Select',
        'Fn::Sub',
        'Fn::And',
        'Fn::Equals',
        'Fn::If',
        'Fn::Not',
        'Fn::Or'
    ]

    def _is_function(self, value):
        return (
            (not self._is_array(value)) and
            (len(value) == 1) and
            (self._get_function_key(value) in self.FUNCTIONS)
        )

    def _get_function_key(self, value):
        return value.keys()[0]

    def _is_array(self, value):
        return isinstance(value, (list, tuple))
