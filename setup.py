from distutils.core import setup

setup(
    name='cfn-json-to-yaml',
    version='1.0',
    packages=['cfnjsontoyaml'],
    url='',
    license='LGPL',
    author='Drew J. Sonne',
    author_email='drew.sonne@gmail.com',
    description='',
    entry_points={
        'console_scripts': [
            'cfn-json-to-yaml=cfnjsontoyaml.__main__:convert'
        ]
    },
    install_requires=[
        'pyyaml'
    ],

)
