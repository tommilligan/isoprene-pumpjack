#!/usr/bin/env python
'''
Provide a JSON serialized graph object, containing all or part
of the full graph available in the backend.

JSON responses are given in the format:
'''

from flask_restful import Resource

from isoprene_pumpjack.constants.environment import bolt_driver
import isoprene_pumpjack.utils as utils
from isoprene_pumpjack.utils.dolphins import dolphins


def reset_graph():
    with bolt_driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")


def set_graph(data):
    with bolt_driver.session() as session:
        for node in data["nodes"]:
            session.run("CREATE (a:Dolphin {id: {id}, label: {label}})",
                        node)

        for link in data["links"]:
            session.run("""MATCH (s:Dolphin {id: {source}}), (t:Dolphin {id: {target}})
                        CREATE (s)-[:knows]->(t)""",
                        link)


class ResetDolphins(Resource):
    '''Debug endpoint - set neo4j as dolphins graph'''
    def __init__(self):
        self.logger = utils.object_logger(self)

    def get(self):
        '''Drop database and upload dolphins JSON data into Neo4j'''
        self.logger.debug('Resetting neo4j to dolphins')
        reset_graph()
        set_graph(dolphins)
        return {}, 200

class NeoReset(Resource):
    '''Debug endpoint - reset neo4j'''
    def __init__(self):
        self.logger = utils.object_logger(self)

    def get(self):
        '''Drop database'''
        self.logger.debug('Resetting neo4j')
        reset_graph()
        return {}, 200

