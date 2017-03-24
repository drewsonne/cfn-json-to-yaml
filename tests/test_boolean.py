import unittest

from cfnjsontoyaml.__main__ import print_to_string
from cfnjsontoyaml.convertor import ConvertToMediary


class TestJoinToSub(unittest.TestCase):
    def test_not(self):
        mediary = ConvertToMediary({
            'Hallo': {
                'Fn::Not': ['ConditionName']
            }
        }).convert()

        self.assertEqual(print_to_string(mediary), """---
Hallo: !Not [ConditionName]
""")
