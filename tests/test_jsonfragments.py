import json
import unittest

import pkg_resources
import re
import yaml
from os.path import basename
from os.path import splitext

from cfnjsontoyaml.__main__ import print_to_string
from cfnjsontoyaml.convertor import ConvertToMediary
from tests.data_provider import data_provider


def dataprovider_fragments():
    fragment_files = pkg_resources.resource_listdir(__name__, 'resources/fragments')
    fragment_basenames = map(lambda file: splitext(basename(file))[0], fragment_files)
    fragment_parts = list(set(fragment_basenames))  # Make unique
    fragment_parts.sort()

    def build_struct(name):
        return (
            name,
            json.loads(pkg_resources.resource_string(__name__, 'resources/fragments/{0}.json'.format(name))),
            # We don't parse the yaml as we're testing the strings are equal
            pkg_resources.resource_string(__name__, 'resources/fragments/{0}.yaml'.format(name))
        )

    return map(build_struct, fragment_parts)


class TestJsonFragments(unittest.TestCase):
    @data_provider(dataprovider_fragments)
    def test_fragments(self, name, json_source, yaml_target):
        mediary = ConvertToMediary(json_source).convert(order_template=True)
        if 'SUBSTITUTIONPLACEHOLDER' in yaml_target:
            matching_pattern = re.escape(yaml_target).replace('SUBSTITUTIONPLACEHOLDER', "[\d\w]{8}")

            self.assertRegexpMatches(
                print_to_string(mediary),
                matching_pattern,
                "Regexp didn't match in fragment '{name}'".format(name=name)
            )
        else:
            self.assertEqual(yaml_target, print_to_string(mediary))
