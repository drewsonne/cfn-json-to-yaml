from unittest import TestCase

import yaml

from cfnjsontoyaml.convertor import ConvertToMediary


class TestTransform(TestCase):
    def test_simple_join(self):
        mediary = ConvertToMediary({
            "Fn::Join": [":", ["NameSpace", {"Ref": "MyVariable"}, {"Ref": "AWS::Region"}]]
        }).convert()

        self.assertEqual(
            yaml.dump(mediary),
            "!Sub \"NameSpace:${MyVariable}:${AWS::Region}\"\n"
        )

    def test_nested_join(self):
        mediary = ConvertToMediary({
            "Fn::Join": [":", [
                "NameSpace",
                {"Ref": "MyVariable"},
                {"Fn::Join": ["", [{"Ref": "AWS::Region"}, "a"]]}
            ]]
        }).convert()

        self.assertEqual(
            yaml.dump(mediary),
            "!Sub \"NameSpace:${MyVariable}:${AWS::Region}a\"\n"
        )

    def test_nested_complex_join(self):
        mediary = ConvertToMediary({
            "Fn::Join": [":", [
                "NameSpace",
                {"Ref": "MyVariable"},
                {"Fn::FindInMap": ["one", "two", "three"]}
            ]]
        }).convert()

        self.assertEqual(
            ("!Sub [\':\', [NameSpace, !Ref \"MyVariable\", !FindInMap [one, two, three]]]\n"),
            yaml.dump(mediary)
        )
