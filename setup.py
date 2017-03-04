#!/usr/bin/env python

import re
from os import path
from setuptools import setup, find_packages


version_file = path.join(
    path.dirname(__file__),
    'isoprene_pumpjack',
    '__version__.py'
)
with open(version_file, 'r') as fp:
    m = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]",
        fp.read(),
        re.M
    )
    version = m.groups(1)[0]

version_file = path.join(
    path.dirname(__file__),
    'isoprene_pumpjack',
    '__version__.py'
)
with open(version_file, 'r') as fp:
    m = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]",
        fp.read(),
        re.M
    )
    version = m.groups(1)[0]


setup(
    name='isoprene-pumpjack',
    version=version,
    license='Apache License 2.0',
    url='https://github.com/tommilligan/isoprene-pumpjack/',
    author='Tom Milligan',
    author_email='tom@tommilligan.net',
    description="Backend for synaptic-scout; request data from Neo4j, perform searches in Elastic, and pump data between the two.",
    keywords='neo neo4j elastic elasticsearch graph iterative',
    packages=find_packages(exclude=['tests']),
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: Apache Software License',
    ],
    zip_safe=False,
    platforms='any',
    test_suite='nose2.collector.collector',
    install_requires=[
        'Flask ~= 0.12',
        'Flask-RESTful ~= 0.3.5',
        'Flask-cors ~= 3.0.2',
        'gunicorn ~= 19.6.0',
        'neo4j-driver ~= 1.1.2'
    ],
    tests_require=['nose2'],
    # Install these with "pip install -e isoprene_pumpjack[dev]
    extras_require={
        'docs': [
            'sphinx',
            'sphinx-argparse',
            'sphinx-rtdtheme',
            'sphinxcontrib-httpdomain'
        ]
    },
    entry_points={
        'console_scripts': [
            'isoprene-pumpjack = isoprene_pumpjack.api:main'
        ]
    },
)
