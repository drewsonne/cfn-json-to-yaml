import unittest

import sys

from six import StringIO

from cfnjsontoyaml.__main__ import print_to_string, convert


class TestMain(unittest.TestCase):
    def test_output(self):
        result = print_to_string({
            'test': 'hallo'
        })
        self.assertEqual(
            "--- {test: hallo}\n",
            result
        )

    def test_cli_no_args(self):
        # Mock the stdin.
        stdin_backup = sys.stdin
        sys.stdin = [
            '{',
            '    "test": "hallo"',
            '}'
        ]

        #Mock the output.
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()

        convert([])
        self.assertEqual(
            "--- {test: hallo}\n\n",
            mystdout.getvalue()
        )

        sys.stdout = old_stdout
        sys.stdin = stdin_backup
