import unittest

import yaml

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
        builder = SubBuilder('_', [
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
        ])
        pattern, substitutions = builder.build()
        self.assertRegexpMatches(pattern, r'one_\$\{fnimportvalue_\w{8}\}_three')
        self.assertEqual(
            """Fn::ImportValue:
  !Sub ${Environment}:vpc_id
            """,
            yaml.dump(substitutions.values()[0])
        )
