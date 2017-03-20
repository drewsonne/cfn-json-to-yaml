from setuptools import setup

__version__ = '1.0.0'

setup(
    name='cfnjsontoyaml',
    version=__version__,
    packages=['cfnjsontoyaml'],
    url='https://github.com/drewsonne/cfn-json-to-yaml',
    download_url='https://github.com/drewsonne/cfn-json-to-yaml/archive/v.{0}.zip'.format(__version__),  # I'll explain this in a second
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
