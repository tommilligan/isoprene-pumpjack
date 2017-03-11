#!/usr/bin/env python
'''
Provide the JSON object to configure synaptic-scout with the
isoprene_pumpjack backend
'''

from flask_restful import Resource

from isoprene_pumpjack.utils import object_logger


config = {
    'endpoints': [
        {
            'name': 'subgraphs',
            'on': 'clickNode',
            'url': '/subgraphs',
        }
    ],
    'types': [
        {
            'type': '_default',
            'typeLabel': 'Dolphin',
            'id': 'id',
            'label': 'label',
            'color': '#42cef4'
        }
    ]
}


class SynapticScoutConfig(Resource):
    '''API endpoint to provide config JSON for synaptic-scout'''
    def __init__(self):
        self.logger = object_logger(self)

    def get(self):
        '''Get JSON config for synaptic-scout'''
        self.logger.debug('Getting config')
        return config, 200

