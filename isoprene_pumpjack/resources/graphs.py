#!/usr/bin/env python
'''
Provide a JSON serialized graph object, containing all or part
of the full graph available in the backend.

JSON responses are given in the format:
```
{
  nodes: [
    { id: 'n0' },
    { id: 'n1' }
  ],
  links: [
    {
      id: 'e0',
      source: 'n0',
      target: 'n1'
    }
  ]
}
```
'''

import os
import random
import json

from flask_restful import Resource

from isoprene_pumpjack.utils import object_logger
from isoprene_pumpjack.utils.dolphins import dolphins


def get_full_graph():
    '''Transparently pass all dolphins data'''
    return dolphins

def get_sub_graph(central_node_id):
    '''Quick and dirty subgraph - throw away most nodes and corresponding links
    '''
    nodes_subset = random.sample(dolphins['nodes'], 7)
    subset = {
        'nodes': nodes_subset,
        'links': dolphins['links']
    }
    return subset


class SubGraph(Resource):
    '''API endpoint to provide config JSON for synaptic-scout'''
    def __init__(self):
        self.logger = object_logger(self)

    def get(self, central_node_id):
        '''Get JSON representing subgraph centered on a single node'''
        self.logger.debug('Getting sub graph for {0}'.format(central_node_id))
        sub_graph = get_sub_graph(central_node_id)
        return sub_graph


class FullGraph(Resource):
    '''Provide all graph data from backend'''
    def __init__(self):
        self.logger = object_logger(self)

    def get(self):
        '''Get JSON representing full graph'''
        self.logger.debug('Getting full graph')
        full_graph = get_full_graph()
        return full_graph
