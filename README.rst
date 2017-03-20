|PyPI version|

|Code Issues|

|codecov|

|Build Status|

cfnjsontoyaml
=============

Convert JSON CloudFormation templates to YAML.

This would automatically convert ``Fn::Join`` functions to ``!Sub``, and
do its best to take advantage of the new tags.

Usage
-----

``cfn-json-to-yaml`` reads either from standard in, or takes the first
argument as the template to ingest and prints the yaml converted
template to stdout.

::

    $ pip install cfnjsontoyaml
    $ cat my_template.json | cfn-json-to-yaml

Problems
--------

There are a wide range of combinations for functions in cloudformation.
If you come across a template which does not render correctly, please
try and isolate the fragment of json which is causing issues, and create
an issue.

.. |PyPI version| image:: https://badge.fury.io/py/cfnjsontoyaml.svg
   :target: https://badge.fury.io/py/cfnjsontoyaml
.. |Code Issues| image:: https://www.quantifiedcode.com/api/v1/project/b6d9757c91b64831ba12fd7cf53332de/badge.svg
   :target: https://www.quantifiedcode.com/app/project/b6d9757c91b64831ba12fd7cf53332de
.. |codecov| image:: https://codecov.io/gh/drewsonne/cfn-json-to-yaml/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/drewsonne/cfn-json-to-yaml
.. |Build Status| image:: https://travis-ci.org/drewsonne/cfn-json-to-yaml.svg?branch=master
   :target: https://travis-ci.org/drewsonne/cfn-json-to-yaml
