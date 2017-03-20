import textwrap
from unittest import TestCase

import re
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

        matching_pattern = re.escape(textwrap.dedent("""        !Sub
        - NameSpace:${MyVariable}:${findinmap_SUBSTITUTIONPLACEHOLDER}
        - findinmap_SUBSTITUTIONPLACEHOLDER: !FindInMap [one, two, three]
        """)).replace("SUBSTITUTIONPLACEHOLDER", "[\d\w]{8}")

        self.assertRegexpMatches(yaml.dump(mediary), matching_pattern)
