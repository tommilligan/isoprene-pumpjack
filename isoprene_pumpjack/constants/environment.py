#!/usr/bin/env python
"""
Environment specific constants for the app
"""

import os

from neo4j.v1 import GraphDatabase, basic_auth
from elasticsearch_dsl.connections import connections

# Neo
ISOPRENE_PUMPJACK_BOLT_URL = os.getenv('GRAPHENEDB_BOLT_URL', 'bolt://localhost:7687')
ISOPRENE_PUMPJACK_BOLT_USER = os.getenv('GRAPHENEDB_BOLT_USER', 'isoprenepumpjack')
ISOPRENE_PUMPJACK_BOLT_PASSWORD = os.getenv('GRAPHENEDB_BOLT_PASSWORD', 'isoprenepumpjack')

bolt_driver = GraphDatabase.driver(
    ISOPRENE_PUMPJACK_BOLT_URL,
    auth=basic_auth(
        ISOPRENE_PUMPJACK_BOLT_USER,
        ISOPRENE_PUMPJACK_BOLT_PASSWORD
    )
)

# Elastic
ISOPRENE_PUMPJACK_ELASTICSEARCH_URL = os.getenv('BONSAI_URL', 'http://localhost:9200/')

# Set default global connection in library
connections.create_connection(hosts=[ISOPRENE_PUMPJACK_ELASTICSEARCH_URL], timeout=500)

