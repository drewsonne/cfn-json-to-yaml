[![PyPI version](https://badge.fury.io/py/cfnjsontoyaml.svg)](https://badge.fury.io/py/cfnjsontoyaml)

[![Code Issues](https://www.quantifiedcode.com/api/v1/project/b6d9757c91b64831ba12fd7cf53332de/badge.svg)](https://www.quantifiedcode.com/app/project/b6d9757c91b64831ba12fd7cf53332de)

[![codecov](https://codecov.io/gh/drewsonne/cfn-json-to-yaml/branch/master/graph/badge.svg)](https://codecov.io/gh/drewsonne/cfn-json-to-yaml)

[![Build Status](https://travis-ci.org/drewsonne/cfn-json-to-yaml.svg?branch=master)](https://travis-ci.org/drewsonne/cfn-json-to-yaml)


# cfnjsontoyaml
Convert JSON CloudFormation templates to the new YAML syntax. This
includes converting all `Fn::*` and `Ref` JSON functions to `!*` yaml
node type functions.

In addition, cfnjsontoyaml tries to make a best guess at when
 `Fn::Join` functions should automatically be converted to `!Sub`.

## Usage
`cfn-json-to-yaml` reads either from standard in, or takes the first
argument as the template to ingest and prints the yaml converted
template to stdout.

    $ pip install cfnjsontoyaml
    $ cat my_template.json | cfn-json-to-yaml

## Problems
There are a wide range of combinations for functions in cloudformation.
If you come across a template which does not render correctly, please
try and isolate the fragment of json which is causing issues, and
create an [issue in github](https://github.com/drewsonne/cfn-json-to-yaml/issues/new) .

If you'd like to be a bit more helpful, you can fork the repository,
create a branch, and add a json/yaml snippet to https://github.com/drewsonne/cfn-json-to-yaml/tree/master/tests/resources/fragments
with the next sequential number. The smaller the json/yaml snippet
you can provide the quicker I can fix it. :-)
