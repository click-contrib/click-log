#!/usr/bin/env python

import ast
import re

from setuptools import setup

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('click_log/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
    name='click-log',
    version=version,
    description='Logging integration for Click',
    author='Markus Unterwaditzer',
    author_email='markus@unterwaditzer.net',
    url='https://github.com/click-contrib/click-log',
    license='MIT',
    long_description=open('README.rst').read(),
    packages=['click_log'],
    install_requires=[
        'click',
    ],
)
