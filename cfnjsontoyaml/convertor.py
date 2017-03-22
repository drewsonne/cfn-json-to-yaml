from collections import OrderedDict

import yaml

from cfnjsontoyaml.mixins import FUNCTION_MAPPING
from cfnjsontoyaml.mixins.type_checker import TypeChecker
from cfnjsontoyaml.parser.subbuilder import SubBuilder
from cfnjsontoyaml.yamlobject.ordereddict import represent_ordereddict  # not directly used, but don't delete


class ConvertToMediary(TypeChecker):
    ROOT_ORDER = [
        'AWSTemplateFormatVersion', 'Transform', 'Description', 'Metadata',
        'Parameters', 'Mappings', 'Conditions', 'Resources', 'Outputs'
    ]
    RESOURCE_ORDER = ['Type', 'Properties', 'DependsOn']

    def __init__(self, template):
        self._template = template
        self._mapping = FUNCTION_MAPPING

    def convert(self, order_template=False):
        converted_dict = self.walk_dictionary(self._template)
        if order_template:
            converted_dict = self.sort_template(converted_dict)
        return converted_dict

    def sort_template(self, converted_dict):
        if 'Resources' in converted_dict.keys():
            for resource_name, resource in converted_dict['Resources'].items():
                converted_dict['Resources'][resource_name] = self.set_dict_order(resource, self.RESOURCE_ORDER)
        return self.set_dict_order(converted_dict, self.ROOT_ORDER)

    @staticmethod
    def set_dict_order(dictionary, order):
        available_keys = dictionary.keys()
        ordered_dictionary = OrderedDict()
        for key in order:
            if key in available_keys:
                ordered_dictionary[key] = dictionary[key]
                available_keys.remove(key)
        for key in available_keys:
            ordered_dictionary[key] = dictionary[key]
        return ordered_dictionary

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
                if str(key) in self.FUNCTIONS:
                    if str(key) == 'Fn::Join':
                        parsed_value = SubBuilder(*parsed_value).build()
                    else:
                        parsed_value = value
                    parsed_value = self._mapping[key](parsed_value)
                else:
                    parsed_value = value
                parsed_dictionary[key] = self.walk_dictionary(value, use_literal=(key in self.FUNCTIONS))
            elif value_type in [str, unicode]:
                if str(key) in self.FUNCTIONS:
                    if str(key) == 'Fn::Join':
                        parsed_value = SubBuilder(*parsed_value).build()
                    else:
                        parsed_value = value
                    return self._mapping[str(key)](parsed_value)
                else:
                    parsed_dictionary[key] = value
            elif value_type == list:
                parsed_value = self.walk_list(value)
                kwargs = {}
                if str(key) in self.FUNCTIONS:
                    child_is_function = self.check_list_has_functions(parsed_value)
                    kwargs['use_literal'] = (use_literal | child_is_function)
                    if str(key) == 'Fn::Join':
                        key = 'Fn::Sub'
                        parsed_value = SubBuilder(*parsed_value).build()
                        return self._mapping[str(key)](parsed_value, **kwargs)
                    else:
                        if kwargs['use_literal']:
                            parsed_dictionary[key] = parsed_value
                        else:
                            return self._mapping[str(key)](parsed_value)
                else:
                    parsed_dictionary[key] = parsed_value
            elif value_type in [bool, int]:
                parsed_dictionary[key] = value
            else:
                raise RuntimeError("Unexpected state with value_type: {0}".format(value_type.__name__))
        return parsed_dictionary

    @staticmethod
    def check_list_has_functions(haystack_list):
        has_function = False
        for item in haystack_list:
            has_function |= issubclass(type(item), yaml.YAMLObject)
        return has_function
