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

    # List of functions, whose arguments are encapsulated in an array
    # This means we can create yaml node types for children of these functions
    ENCAPSULATED_FUNCTIONS = [
        'Fn::And',
        'Fn::Equals',
        'Fn::If',
        'Fn::Not',
        'Fn::Or',
        'Fn::FindInMap',
        "Fn::GetAtt",
        "Fn::Join",
        "Fn::Select",
        "Fn::Split"
    ]

    def _is_function(self, value):
        return (
            (not self._is_array(value)) and
            (len(value) == 1) and
            (self._get_function_key(value) in self.FUNCTIONS)
        )

    @staticmethod
    def _get_function_key(value):
        return value.keys()[0]

    def _is_array(self, value):
        return isinstance(value, (list, tuple))
