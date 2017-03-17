# isoprene-pumpjack

[![PyPI](https://img.shields.io/pypi/pyversions/isoprene-pumpjack.svg)]()
[![Documentation Status](http://isoprene-pumpjack.readthedocs.io/en/master/?badge=master)]()
[![license](https://img.shields.io/github/license/tommilligan/isoprene-pumpjack.svg)]()

[![Travis branch](https://img.shields.io/travis/tommilligan/isoprene-pumpjack/develop.svg)]()
[![Coveralls branch](https://img.shields.io/coveralls/tommilligan/isoprene-pumpjack/develop.svg)]()
[![Code Climate](https://img.shields.io/codeclimate/github/tommilligan/isoprene-pumpjack.svg)]()
[![Requirements Status](https://requires.io/github/tommilligan/isoprene-pumpjack/requirements.svg?branch=develop)]()


## Installation

Install using pip
```
pip install isoprene-pumpjack
```

Run using
```
isoprene-pumpjack
```

## Required services

Configuration is via environment variables

* Neo4j
    * ISOPRENE_PUMPJACK_BOLT_URL (*default: bolt://localhost:7687*)
    * ISOPRENE_PUMPJACK_BOLT_USER (*default: isoprenepumpjack*)
    * ISOPRENE_PUMPJACK_BOLT_PASSWORD (*default: isoprenepumpjack*)
* Elasticsearch
    * ISOPRENE_PUMPJACK_ELASTICSEARCH_URL (*default: http://localhost:9200/*)
