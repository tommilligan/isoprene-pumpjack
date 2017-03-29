# isoprene-pumpjack

[![PyPI](https://img.shields.io/pypi/v/isoprene-pumpjack.svg)](https://pypi.python.org/pypi/isoprene-pumpjack)
[![PyPI](https://img.shields.io/pypi/pyversions/isoprene-pumpjack.svg)](https://pypi.python.org/pypi/isoprene-pumpjack)
[![Documentation Status](https://readthedocs.org/projects/isoprene-pumpjack/badge/?version=master)](http://isoprene-pumpjack.readthedocs.io/en/master/?badge=master)
[![license](https://img.shields.io/github/license/tommilligan/isoprene-pumpjack.svg)](https://pypi.python.org/pypi/isoprene-pumpjack)

[![Travis branch](https://img.shields.io/travis/tommilligan/isoprene-pumpjack/develop.svg)](https://travis-ci.org/tommilligan/isoprene-pumpjack)
[![codecov](https://codecov.io/gh/tommilligan/isoprene-pumpjack/branch/develop/graph/badge.svg)](https://codecov.io/gh/tommilligan/isoprene-pumpjack)
[![Code Climate](https://img.shields.io/codeclimate/github/tommilligan/isoprene-pumpjack.svg)](https://codeclimate.com/github/tommilligan/isoprene-pumpjack/)
[![Requirements Status](https://requires.io/github/tommilligan/isoprene-pumpjack/requirements.svg?branch=develop)](https://codeclimate.com/github/tommilligan/synaptic-scout/)


## Installation

Install using pip
```
pip install isoprene-pumpjack
```

Run in development:
```
isoprene-pumpjack
```
or in production:
```
gunicorn isoprene_pumpjack.wsgi:app
```

## Required services

Configuration is via environment variables

* Neo4j
    * ISOPRENE_PUMPJACK_BOLT_URL (*default: bolt://localhost:7687*)
    * ISOPRENE_PUMPJACK_BOLT_USER (*default: isoprenepumpjack*)
    * ISOPRENE_PUMPJACK_BOLT_PASSWORD (*default: isoprenepumpjack*)
* Elasticsearch
    * ISOPRENE_PUMPJACK_ELASTICSEARCH_URL (*default: http://localhost:9200/*)


## Documentation

The full documentation is available [here on readthedocs](http://isoprene-pumpjack.readthedocs.io/en/master/)

