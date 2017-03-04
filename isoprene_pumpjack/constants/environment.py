#!/usr/bin/env python
"""
Environment specific constants for the app
"""

import os

from neo4j.v1 import GraphDatabase, basic_auth


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

