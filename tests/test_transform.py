from unittest import TestCase

import yaml

from cfnjsontoyaml.convertor import ConvertToMediary


class TestTransform(TestCase):
    def test_to_yaml_ref(self):
        mediary = ConvertToMediary({
            'Resources': {
                'MyYamlResource': {
                    'Type': 'AWS::S3::Bucket',
                    'Properties': {
                        'Name': {
                            'Ref': 'MyVariable'
                        }
                    }
                }
            }
        }).convert()

        self.assertEquals(
            ("Resources:\n"
             "  MyYamlResource:\n"
             "    Properties:\n"
             "      Name: !Ref \"MyVariable\"\n"
             "    Type: AWS::S3::Bucket\n"),
            yaml.dump(mediary)
        )

    def test_to_yaml_join_to_sub(self):
        median = ConvertToMediary({
            'Resources': {
                'MyYamlResource': {
                    'Type': 'AWS::S3::Bucket',
                    'Properties': {
                        'Name': {
                            "Fn::Join": [":", ["NameSpace", {"Ref": "MyVariable"}]]
                        }
                    }
                }
            }
        }).convert()

        self.assertEquals(
            ("Resources:\n"
             "  MyYamlResource:\n"
             "    Properties:\n"
             "      Name: !Sub \"NameSpace:${MyVariable}\"\n"
             "    Type: AWS::S3::Bucket\n"),
            yaml.dump(median)
        )
