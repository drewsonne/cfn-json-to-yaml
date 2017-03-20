from unittest import TestCase

import yaml
from cfnjsontoyaml.convertor import ConvertToMediary


class TestRef(TestCase):
    def test_simple_ref(self):
        mediary = ConvertToMediary({
            "Ref": "MyVariable"
        }).convert()


        self.assertEqual(
            yaml.dump(mediary),
            "!Ref \"MyVariable\"\n"
        )
