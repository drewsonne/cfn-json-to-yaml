import textwrap
import unittest

import re
import yaml

from cfnjsontoyaml.convertor import ConvertToMediary
from cfnjsontoyaml.parser.subbuilder import SubBuilder


class TestJoinToSub(unittest.TestCase):
    def test_string_join_to_string(self):
        builder = SubBuilder('-', ['one', 'two', 'three'])
        self.assertEqual(builder.build()[0], 'one-two-three')
        self.assertIsNone(builder.build()[1])

    def test_ref_join_to_string(self):
        builder = SubBuilder('_', ['one', {'Ref': 'two'}, 'three'])
        self.assertEqual(builder.build()[0], 'one_${two}_three')
        self.assertIsNone(builder.build()[1])

    def test_attr_joint_to_string(self):
        builder = SubBuilder('.', ['one', {'Fn::GetAtt': ['two', 'three']}, 'four'])
        self.assertEqual(builder.build()[0], 'one.${two.three}.four')
        self.assertIsNone(builder.build()[1])

    def test_importvalue_to_string(self):
        builder = SubBuilder('_', [
            'one',
            {'Fn::ImportValue': 'two'},
            'three'
        ])
        pattern, substitutions = builder.build()
        self.assertRegexpMatches(pattern, r'one_\$\{fnimportvalue_\w{8}\}_three')
        self.assertEqual(substitutions.values()[0], {
            'Fn::ImportValue': 'two'
        })

    def test_importvalue_with_ref_to_string(self):
        mediary = ConvertToMediary({'Fn::Join': ['_', [
            'one',
            {
                'Fn::ImportValue': {'Fn::Join': [
                    ':',
                    [
                        {'Ref': 'Environment'},
                        'vpc_id'
                    ]
                ]}},
            'three'
        ]]}).convert()

        matching_pattern = re.escape(textwrap.dedent("""                !Sub
                - one_${fnimportvalue_SUBSTITUTIONPLACEHOLDER}_three
                - fnimportvalue_SUBSTITUTIONPLACEHOLDER:
                    Fn::ImportValue: !Sub "${Environment}:vpc_id"
                """)).replace("SUBSTITUTIONPLACEHOLDER", "[\d\w]{8}")

        self.assertRegexpMatches(yaml.dump(mediary), matching_pattern)
