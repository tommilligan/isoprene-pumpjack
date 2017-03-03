#!/usr/bin/env python
'''
Provide a JSON serialized list of endpoints
'''

from flask_restful import Resource

from isoprene_pumpjack.utils import object_logger

discovery = {
  "kind": "discovery#restDescription",
  "discoveryVersion": "v1",
  "id": 'isoprene-pumpjack:v1',
  "name": 'isoprene-pumpjack',
  "version": 'v1',
  "revision": '1',
  "title": 'Isoprene Pumpjack',
  "description": 'Backend for synaptic-scout; request data from Neo4j, perform searches in Elastic, and pump data between the two.',
  "documentationLink": "https://isoprene-pumpjack.readthedocs.io/",
}


class Discovery(Resource):
    '''API endpoint to provide config JSON for synaptic-scout'''
    def __init__(self):
        self.logger = object_logger(self)

    def get(self):
        '''Get JSON representing endpoints'''
        self.logger.debug('Getting discovery')
        return discovery
