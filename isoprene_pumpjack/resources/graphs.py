#!/usr/bin/env python
'''
Provide a JSON serialized graph object, containing all or part
of the full graph available in the backend.

JSON responses are given in the format:
'''

from flask_restful import Resource

from isoprene_pumpjack.constants.environment import bolt_driver
import isoprene_pumpjack.utils as utils
import isoprene_pumpjack.utils.neo_to_d3 as neo_to_d3


def get_full_graph():
    '''Transparently pass all database data'''
    with bolt_driver.session() as session:
        result = session.run("""MATCH (d)-[r]-()
                        RETURN d, r""")
    
    data = neo_to_d3.neo_to_d3(result, ["d"], ["r"])
    return data

def get_sub_graph(central_node_id):
    '''Quick and dirty subgraph - throw away most nodes and corresponding links
    '''
    with bolt_driver.session() as session:
        result = session.run("""MATCH (s)-[r*1..2]-(t)
                        WHERE s.id = {id}
                        RETURN s, r, t""",
                        {"id": central_node_id})
    
    data = neo_to_d3.neo_to_d3(result, ["s", "t"], ["r"])
    return data


class SubGraph(Resource):
    '''API endpoint to provide config JSON for synaptic-scout'''
    def __init__(self):
        self.logger = utils.object_logger(self)

    def get(self, central_node_id):
        '''Get JSON representing subgraph centered on a single node'''
        self.logger.debug('Getting sub graph for {0}'.format(central_node_id))
        sub_graph = get_sub_graph(central_node_id)
        return sub_graph, 200


class FullGraph(Resource):
    '''Provide all graph data from backend'''
    def __init__(self):
        self.logger = utils.object_logger(self)

    def get(self):
        '''Get JSON representing full graph'''
        self.logger.debug('Getting full graph')
        full_graph = get_full_graph()
        return full_graph, 200
