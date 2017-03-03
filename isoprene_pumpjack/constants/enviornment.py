#!/usr/bin/env python
"""
Environment specific constants for the app
"""

ISOPRENE_PUMPJACK_GRAPH_DB_URL = os.getenv('ISOPRENE_PUMPJACK_GRAPH_DB_URL', 'localhost:7474')
ISOPRENE_PUMPJACK_GRAPH_DB_USER = os.getenv('ISOPRENE_PUMPJACK_GRAPH_DB_USER', 'isoprenepumpjack')
ISOPRENE_PUMPJACK_GRAPH_DB_PASSWORD = os.getenv('ISOPRENE_PUMPJACK_GRAPH_DB_PASSWORD', 'isoprenepumpjack')
