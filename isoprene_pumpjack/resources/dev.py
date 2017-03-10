#!/usr/bin/env python
'''
Provide a JSON serialized graph object, containing all or part
of the full graph available in the backend.

JSON responses are given in the format:
'''

from flask_restful import Resource

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q, Index

from isoprene_pumpjack.constants.environment import bolt_driver
import isoprene_pumpjack.utils as utils
from isoprene_pumpjack.utils.dolphins import dolphins
from isoprene_pumpjack.resources.search import Dolphin, DolphinSighting


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


def reset_elastic():
    '''Drop all elastic indexes'''
    i = Index('_all')
    response = i.delete()
    return response

def create_dolphins_index():
    i = Index('dolphins')

    # create the index, including DocType mappings
    i.create()

    for link in dolphins["links"]:
        # instantiate the document
        pairing_report = DolphinSighting()
        # assign some field values, can be values or lists of values
        pairing_report.dolphins = [
            list((x['label'] for x in dolphins['nodes']
                        if x["id"] == link["source"]))[0],
            list((x["label"] for x in dolphins['nodes']
                        if x["id"] == link["target"]))[0]
        ]

        # save the document into the cluster
        pairing_report.save()


class ElasticReset(Resource):
    '''Debug endpoint - reset elastic'''
    def __init__(self):
        self.logger = utils.object_logger(self)

    def get(self):
        '''Drop database'''
        self.logger.debug('Resetting elastic')
        response = reset_elastic()
        return response, 200


class IndexDolphins(Resource):
    '''Debug endpoint - create an Elastic dolphins index'''
    def __init__(self):
        self.logger = utils.object_logger(self)

    def get(self):
        '''Create and load dolphins index'''
        self.logger.debug('Indexing dolphins in elastic')
        reset_elastic()
        response = create_dolphins_index()
        return response, 200


