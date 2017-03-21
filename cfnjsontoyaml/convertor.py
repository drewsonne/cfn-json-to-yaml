import yaml

from cfnjsontoyaml.mixins import FUNCTION_MAPPING
from cfnjsontoyaml.mixins.type_checker import TypeChecker
from cfnjsontoyaml.parser.subbuilder import SubBuilder


class ConvertToMediary(TypeChecker):
    def __init__(self, template):
        self._template = template
        self._mapping = FUNCTION_MAPPING

    def convert(self):
        return self.walk_dictionary(self._template)

    def walk_list(self, array):
        parsed_list = []
        for value in array:
            value_type = type(value)
            if value_type == dict:
                parsed_list.append(self.walk_dictionary(value))
            elif value_type in [str, unicode]:
                parsed_list.append(value)
            elif value_type == list:
                parsed_list.append(self.walk_list(value))
            else:
                parsed_list.append(value)
        return parsed_list

    def walk_dictionary(self, dictionary, use_literal=False):
        parsed_dictionary = {}
        for key, value in dictionary.items():
            value_type = type(value)
            if value_type == dict:
                if key in self.FUNCTIONS:
                    if key == 'Fn::Join':
                        parsed_value = SubBuilder(*parsed_value).build()
                    else:
                        parsed_value = value
                    parsed_value = self._mapping[key](parsed_value)
                else:
                    parsed_value = value
                parsed_dictionary[key] = self.walk_dictionary(value, use_literal=(key == 'Fn::Base64'))
            elif value_type in [str, unicode]:
                if key in self.FUNCTIONS:
                    if key == 'Fn::Join':
                        parsed_value = SubBuilder(*parsed_value).build()
                    else:
                        parsed_value = value
                    return self._mapping[str(key)](parsed_value)
                else:
                    parsed_dictionary[key] = value
            elif value_type == list:
                parsed_value = self.walk_list(value)
                kwargs = {}
                if key in self.FUNCTIONS:
                    if str(key) == 'Fn::Join':
                        key = 'Fn::Sub'
                        parsed_value = SubBuilder(*parsed_value).build()
                        kwargs['use_literal'] = use_literal
                        return self._mapping[str(key)](parsed_value, **kwargs)
                    else:
                        return self._mapping[str(key)](parsed_value)

                else:
                    parsed_dictionary[key] = value
            else:
                value
        return parsed_dictionary
