import textwrap
from unittest import TestCase

import re
import yaml

from cfnjsontoyaml.convertor import ConvertToMediary


class TestComplextransform(TestCase):
    def test_complextransform(self):
        mediary = ConvertToMediary({
            'Resources': {
                'MyYamlResource': {
                    'Type': 'AWS::S3::Bucket',
                    'Properties': {
                        'RefProp': {
                            "Fn::Join": [":", ["NameSpace", {"Ref": "MyVariable"}]]
                        },
                        'FindInMapProp': {
                            "Fn::FindInMap": ["MapName", "TopLevelKey", "SecondLevelKey"]
                        },
                        'GetAttrProp': {
                            "Fn::GetAtt": ["MyResourceName", "Attribute"]
                        },
                    }
                }
            }
        }).convert()

        self.assertEqual(
            "Resources:\n"
            "  MyYamlResource:\n"
            "    Properties:\n"
            "      FindInMapProp: !FindInMap [MapName, TopLevelKey, SecondLevelKey]\n"
            "      GetAttrProp: !GetAtt \"MyResourceName.Attribute\"\n"
            "      RefProp: !Sub \"NameSpace:${MyVariable}\"\n"
            "    Type: AWS::S3::Bucket\n",
            yaml.dump(mediary)
        )

        # 'SelectMapping': {
        #     "Fn::Join": [
        #         "", [
        #             {
        #                 "Fn::Select": [
        #                     "eu-west-1a",
        #                     {
        #                         "Fn::GetAZs": "eu-west-1"
        #                     }
        #                 ]
        #             },
        #             "Testing",
        #             {
        #                 "Ref": "MyVar"
        #             }
        #         ]
        #     ]
        #
        # }

    def test_complextransform_userdata(self):
        mediary = ConvertToMediary({
            'Resources': {
                'MyYamlResource': {
                    'Type': 'AWS::S3::Bucket',
                    'Properties': {
                        'UserData': {
                            "Fn::Base64": {
                                "Fn::Join": [
                                    "", [
                                        "#! /bin/bash -xe\n",
                                        "yum install -y aws-cfn-bootstrap\n",

                                        "# Install the files and packages from the metadata\n",
                                        "/opt/aws/bin/cfn-init -v ",
                                        "--stack ", {"Ref": "AWS::Region"},
                                        " --resource ", {
                                            "Fn::FindInMap": ["MapName", "TopLevelKey", "SecondLevelKey"]
                                        },
                                        " --configsets ", {"Fn::Select": [0, ["one", "two"]]}, " ",
                                        "--region ", {"Ref": "AWS::Region"}
                                    ]
                                ]
                            }
                        }
                    }
                }
            }
        }).convert()

        matching_pattern = re.escape(textwrap.dedent("""             Resources:
               MyYamlResource:
                 Properties:
                   UserData:
                     Fn::Base64: !Sub
                     - |-
                       #! /bin/bash -xe
                       yum install -y aws-cfn-bootstrap
                       # Install the files and packages from the metadata
                       /opt/aws/bin/cfn-init -v --stack ${AWS::Region} --resource ${findinmap_SUBSTITUTIONPLACEHOLDER} --configsets ${select_SUBSTITUTIONPLACEHOLDER} --region ${AWS::Region}
                     - findinmap_SUBSTITUTIONPLACEHOLDER: !FindInMap [MapName, TopLevelKey, SecondLevelKey]
                       select_SUBSTITUTIONPLACEHOLDER: !Select [0, [one, two]]
                 Type: AWS::S3::Bucket
             """)).replace('SUBSTITUTIONPLACEHOLDER', "[\d\w]{8}")
        self.assertRegexpMatches(yaml.dump(mediary), matching_pattern)
