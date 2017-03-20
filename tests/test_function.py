import textwrap

import yaml, re, unittest

from cfnjsontoyaml.convertor import ConvertToMediary


class TestBasicFunctions(unittest.TestCase):
    def test_complexjoin(self):
        mediary = ConvertToMediary({
            'Resources': {
                'MyResources': {
                    'Type': 'AWS::EC2::Instance',
                    'Properties': {
                        'UserData': {
                            "Fn::Base64": {
                                "Fn::Join": [
                                    "",
                                    [
                                        "#!/bin/bash\n",
                                        "# bootstrap/default-cloud-init.sh\n",
                                        "sudo easy_install https://s3.amazonaws.com/cloudformation-examples/aws-cfn-bootstrap-latest.tar.gz;\n",
                                        "/usr/local/bin/cfn-signal -e $? --stack \"",
                                        {
                                            "Ref": "AWS::StackName"
                                        },
                                        "\" --resource ",
                                        {
                                            "Fn::ImportValue": "my_external_resource_name"
                                        }
                                        , " --region \"",
                                        {
                                            "Ref": "AWS::Region"
                                        },
                                        "\";\n",
                                        "\n",
                                        "yum -y remove sendmail\n",
                                        "yum -v clean all && yum -v makecache\n",
                                        "yum -v install -y jq yum-cron\n",
                                        "yum -y update\n",
                                        "\n",
                                        "\n",
                                        "aws s3 cp s3://myscripts/bootstrap.sh /root/bootstrap.sh\n",
                                        "chmod a+x /root/bootstrap.sh\n",
                                        "echo \"/root/bootstrap.sh\" >> /etc/rc.local\n",
                                        "reboot\n",
                                        "\n"
                                    ]
                                ]
                            }
                        }
                    }
                }
            }
        }).convert()

        matching_pattern = re.escape(textwrap.dedent("""                Resources:
                  MyResources:
                    Properties:
                      UserData:
                        Fn::Base64: !Sub
                        - |+
                          #!/bin/bash
                          # bootstrap/default-cloud-init.sh
                          sudo easy_install https://s3.amazonaws.com/cloudformation-examples/aws-cfn-bootstrap-latest.tar.gz;
                          /usr/local/bin/cfn-signal -e $? --stack "${AWS::StackName}" --resource ${importvalue_SUBSTITUTIONPLACEHOLDER} --region "${AWS::Region}";

                          yum -y remove sendmail
                          yum -v clean all && yum -v makecache
                          yum -v install -y jq yum-cron
                          yum -y update


                          aws s3 cp s3://myscripts/bootstrap.sh /root/bootstrap.sh
                          chmod a+x /root/bootstrap.sh
                          echo "/root/bootstrap.sh" >> /etc/rc.local
                          reboot

                        - importvalue_SUBSTITUTIONPLACEHOLDER: !ImportValue "my_external_resource_name"
                    Type: AWS::EC2::Instance
                """)).replace("SUBSTITUTIONPLACEHOLDER", "[\d\w]{8}")


        self.assertRegexpMatches(yaml.dump(mediary), matching_pattern)

        def test_longjoin(self):
            mediary = ConvertToMediary({
                'Resources': {
                    'MyResources': {
                        'Type': 'AWS::EC2::Instance',
                        'Properties': {
                            'UserData': {
                                "Fn::Base64": {
                                    "Fn::Join": [
                                        "",
                                        [
                                            "#!/bin/bash\n",
                                            "# bootstrap/default-cloud-init.sh\n",
                                            "sudo easy_install https://s3.amazonaws.com/cloudformation-examples/aws-cfn-bootstrap-latest.tar.gz;\n",
                                            "/usr/local/bin/cfn-signal -e $? --stack \"",
                                            {
                                                "Ref": "AWS::StackName"
                                            },
                                            "\" --resource ASG --region \"",
                                            {
                                                "Ref": "AWS::Region"
                                            },
                                            "\";\n",
                                            "\n",
                                            "yum -y remove sendmail\n",
                                            "yum -v clean all && yum -v makecache\n",
                                            "yum -v install -y jq yum-cron\n",
                                            "yum -y update\n",
                                            "\n",
                                            "\n",
                                            "aws s3 cp s3://pure360-ansible-prod/sysops_ansible_prod.sh /root/sysops_ansible.sh\n",
                                            "chmod a+x /root/sysops_ansible.sh\n",
                                            "echo \"/root/sysops_ansible.sh\" >> /etc/rc.local\n",
                                            "reboot\n",
                                            "\n"
                                        ]
                                    ]
                                }
                            }
                        }
                    }
                }
            }).convert()
            self.assertEqual("""Resources:
  MyResources:
    Properties:
      UserData:
        Fn::Base64: !Sub |+
          #!/bin/bash
          # bootstrap/default-cloud-init.sh
          sudo easy_install https://s3.amazonaws.com/cloudformation-examples/aws-cfn-bootstrap-latest.tar.gz;
          /usr/local/bin/cfn-signal -e $? --stack "${AWS::StackName}" --resource ASG --region "${AWS::Region}";

          yum -y remove sendmail
          yum -v clean all && yum -v makecache
          yum -v install -y jq yum-cron
          yum -y update


          aws s3 cp s3://myscripts/bootstrap.sh /root/bootstrap.sh
          chmod a+x /root/bootstrap.sh
          echo "/root/bootstrap.sh" >> /etc/rc.local
          reboot

    Type: AWS::EC2::Instance
""", yaml.dump(mediary))

        def test_nodeconvertor(self):
            mediary = ConvertToMediary({
                'Resources': {
                    'MyResources': {
                        'Type': 'AWS::S3::Bucket',
                        'Properties': {
                            'Name': {
                                'Ref': 'MyBucketName'
                            },
                            'Tag': {
                                'Fn::ImportValue': {
                                    'Fn::Sub': [
                                        '${Environment}:alpha:beta:gamma',
                                        {
                                            'Environment': {
                                                'Fn::Select': [
                                                    0,
                                                    'MappingName'
                                                ]
                                            }
                                        }
                                    ]
                                }
                            },
                            'JoinToSub': {
                                'Fn::Join': [
                                    '-',
                                    [
                                        'one',
                                        'two',
                                        {'Ref': 'MyRef'},
                                        {'Fn::GetAtt': ['MyRsc', 'Att']}
                                    ]
                                ]
                            }
                        }
                    }
                }
            }).convert()

            self.assertEqual("""Resources:
  MyResources:
    Properties:
      JoinToSub: !Sub "one-two-${MyRef}-${MyRsc.Att}"
      Name: !Ref "MyBucketName"
      Tag:
        Fn::ImportValue: !Sub
        - ${Environment}:alpha:beta:gamma
        - Environment: !Select [0, MappingName]
    Type: AWS::S3::Bucket
""", yaml.dump(mediary))
