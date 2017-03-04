#!/usr/bin/env python
'''
Provide a JSON serialized set of search results.
'''

from flask_restful import Resource

import isoprene_pumpjack.utils as utils


class SearchDolphins(Resource):
    '''API endpoint to provide config JSON for synaptic-scout'''
    def __init__(self):
        self.logger = utils.object_logger(self)

    def get(self, central_node_id):
        '''Get JSON representing subgraph centered on a single node'''
        self.logger.debug('Searching')
        query = request.args.get('q', '')
        return {}, 200

