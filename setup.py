#!/usr/bin/env python3

import re
import os
import sys

from setuptools import setup, find_packages
try:
    from semantic_release import setup_hook

    setup_hook(sys.argv)
except ImportError:
    pass

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    readme = f.read()

with open(os.path.join(here, 'CHANGELOG.md'), encoding='utf-8') as f:
    history = f.read()

dependency_links = []

project_dir = os.path.dirname(os.path.realpath(__file__))

requirements = os.path.join(project_dir, 'requirements.txt')
requirements_dev = os.path.join(project_dir, 'requirements-dev.txt')
requirements_ci = os.path.join(project_dir, 'requirements-ci.txt')

with open(requirements, encoding='utf-8') as f:
    install_requires = list(map(str.strip, f.read().splitlines()))[1:]

with open(requirements_dev, encoding='utf-8') as f:
    dev_require = list(filter(lambda x: '://' not in x, map(str.strip, f.read().splitlines())))[:-1]

with open(requirements_ci, encoding='utf-8') as f:
    ci_require = list(filter(lambda x: '://' not in x, map(str.strip, f.read().splitlines())))[:-1]

dependency_link_pattern = re.compile("(\S+:\/\/\S+)#egg=(\S+)")

dependency_links = []
install_requires_fixed = []
for req in install_requires:
    match = dependency_link_pattern.match(req)
    if match:
        install_requires_fixed.append(match.group(2))
        dependency_links.append(match.group(1))
    else:
        install_requires_fixed.append(req)
install_requires = install_requires_fixed

package_data = []

with open('click_logging/__init__.py', 'r') as f:
    version = re.search(r'^__version__\st*=\s*[\'"]([^\'"]*)[\'"]$', f.read(), re.MULTILINE).group(1)

setup(
    name='click-logging',
    version=version,
    description='Logging integration for Click',
    author='Rémi Alvergnat',
    author_email='toilal.dev@gmail.com',
    url='https://github.com/Toilal/click-logging',
    license='MIT',
    long_description=readme + '\n' * 2 + history,
    long_description_content_type='text/markdown',
    classifiers=[
        # See: https://pypi.python.org/pypi?:action=list_classifiers
        'Development Status :: 5 - Stable',
        'Environment :: Console',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        # List of python versions and their support status:
        # https://en.wikipedia.org/wiki/CPython#Version_history
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: System :: Logging',
    ],
    packages=find_packages(),
    dependency_links=dependency_links,
    include_package_data=True,
    zip_safe=True,
    install_requires=install_requires,
    extras_require={
        'dev': dev_require,
        'ci': ci_require
    }
)
