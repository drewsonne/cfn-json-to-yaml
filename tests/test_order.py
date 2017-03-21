import textwrap
from unittest import TestCase

from cfnjsontoyaml.__main__ import print_to_string
from cfnjsontoyaml.convertor import ConvertToMediary


class TestOrder(TestCase):
    def test_simple_join(self):
        mediary = ConvertToMediary({
            'Outputs': {
                'MyValue1': 'one',
                'AnotherValue': 'two'
            },
            'AWildCard': 'Surprise!',
            'Resources': {
                'FirstResource': {
                    'Properties': {
                        'Property': 'this'
                    },
                    'Type': 'AWS::S3::Bucket',
                    'DependsOn': 'Other'
                }
            },
            'Description': 'This description is in the wrong place'
        }).convert(order_template=True)

        self.assertEqual(textwrap.dedent("""        ---
        Description: This description is in the wrong place
        Resources:
          FirstResource:
            Type: AWS::S3::Bucket
            Properties:
              Property: this
            DependsOn: Other
        Outputs:
          AnotherValue: two
          MyValue1: one
        AWildCard: Surprise!\n"""), print_to_string(mediary))
