# Builds a Sub function from a join.
import random
import string

import re

class SubBuilder(object):
    FUNCTIONS = [
        'Ref',
        # 'Fn::Base64',
        # 'Fn::FindInMap',
        'Fn::GetAtt',
        # 'Fn::GetAZs',
        'Fn::ImportValue',
        'Fn::Join',
        # 'Fn::Select',
        'Fn::Sub'
        # 'Fn::And',
        # 'Fn::Equals',
        # 'Fn::If',
        # 'Fn::Not',
        # 'Fn::Or'
    ]

    def __init__(self, join_token, values):
        self._join_token = join_token
        self._values = values

        # If we have any values which can't be converted to elements in the sub string, put them in here.
        self._string_substitutions = {}
        self._pattern = None

    def build(self):
        # If this is a join then we will have a list of values to join.

        sub_pattern = []
        substitutions = []

        for value in self._values:
            pattern_key, substitution = self.stringify_value(value)
            if substitution is not None:
                substitutions.append(substitution)
            sub_pattern.append(pattern_key)

        string_pattern = self._join_token.join(sub_pattern)

        return string_pattern, dict(substitutions) if len(substitutions) else None

    def stringify_value(self, value):
        value_type = self._get_value_type(value)
        random_key = ''.join(random.choice('abcdef' + string.digits) for _ in range(8))

        if value_type in ['str', 'unicode']:
            return value, None
        elif value_type == 'Ref':
            return '${' + value['Ref'] + '}', None
        elif value_type == 'Fn::GetAtt':
            return '${' + value['Fn::GetAtt'][0] + '.' + value['Fn::GetAtt'][1] + '}', None
        elif value_type in ['Fn::ImportValue']:
            sub_key = re.sub(r'[^a-z]+', '', value_type.lower()) + '_' + random_key
            return '${' + sub_key + '}', (sub_key, value)
        elif value_type in ['!Ref','!GetAtt']:
            return '${' + value.value + '}', None
        elif value_type.startswith('!'):
            if value_type == '!Sub':
                if not value.is_sequence:
                    return value.value, None
            sub_key = re.sub(r'[^a-z]+', '', value.yaml_tag.lower()) + '_' + random_key
            sub_key = sub_key.encode('ascii', 'ignore')
            return '${' + sub_key + '}', (sub_key, value)
        else:
            return value

    # # 1 - do a check to make sure the tree below can be converted
    #     values_are_stringable = self.validate_value_string_conversion()
    #     # 2 - iterate through each element in the values and convert it to a string.
    #     if values_are_stringable:
    #         converted_values = self.convert_values_to_string()
    #
    # def convert_values_to_string(self):
    #
    #
    # def validate_value_string_conversion(self):
    #     all_values_valid = True
    #     for value in self._values:
    #         value_type = self._get_value_type(value)
    #         if value_type == 'str':
    #             all_values_valid &= True
    #         else:
    #             all_values_valid &= False
    #     return all_values_valid

    def _get_value_type(self, value):
        _type = type(value).__name__
        if _type in ['str', 'unicode']:
            return type(value).__name__
        if (_type == 'dict') and (len(value.keys()) == 1) and (value.keys()[0] in self.FUNCTIONS):
            return value.keys()[0]
        try:
            return value.yaml_tag
        except AttributeError as error:
            raise AttributeError("Could not find 'yaml_tag' on {0}:{1}".format(value, type(value).__name__))
