#!/usr/bin/env python

from distutils.core import setup

try:
    license = open('LICENSE').read()
except:
    license = None

try:
    readme = open('README.md').read()
except:
    readme = None

setup(
    name='pyStatParser',
    version='0.0.1',
    author='Emilio Monti',
    author_email='emilmont@gmail.com',
    packages=['stat_parser', 'stat_parser.treebanks'],
    package_data={'stat_parser.treebanks': ['PennTreebank/*', 'QuestionBank/*']},
    scripts=[],
    url='http://github.com/emilmont/pyStatParser/',
    license=license,
    description='Simple Python Statistical Parser',
    long_description=readme,
)
