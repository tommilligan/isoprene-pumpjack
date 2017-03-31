#!/usr/bin/env python
'''
Provide a JSON serialized set of search results.
'''

import logging
import json

from flask import request
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q, Index, DocType, Text, Nested, InnerObjectWrapper

from isoprene_pumpjack.utils import SmartResource
from isoprene_pumpjack.helpers.services import execute_cypher, execute_search

logger = logging.getLogger(__name__)

i = Index('dolphins')

@i.doc_type
class Dolphin(DocType):
    id = Text()
    label = Text()

@i.doc_type
class DolphinSighting(DocType):
    dolphins = Text()


def dolphin_label_hits(label):
    '''Search for all records of a dolphin by label'''
    logger.debug("Searching index for {0}".format(label))
    q = Q('match', dolphins=label)
    s = Search().query(q).index('dolphins').doc_type(DolphinSighting)
    logger.debug('Executing elastic search {0}'.format(s.to_dict()))
    response = execute_search(s)
    logger.debug('Search found {0} results'.format(response.hits.total))
    return response.hits.hits

def merge_hits_to_node(hits):
    '''Collate document records to nodes and links, and upload to neo'''
    logger.debug('Merging {0} elastic documents to neo node'.format(len(hits)))

    # For each document returned by the query, store extraneous data
    for document in hits:
        document_id = document["_id"]
        dolphins = document["_source"]["dolphins"]
        
        for dolphin in dolphins:
            cypher = """MERGE (s:{doc_label} {{ id: '{doc_id}', label: '{doc_id}' }})
                        ON CREATE SET s.isopump_load_initial = timestamp(), s.isopump_fully_loaded = TRUE
                        ON MATCH SET s.isopump_load_last = timestamp()
                        MERGE (d:{neo_label} {{ id: '{peripheral_id}', label: '{peripheral_id}' }})
                        ON CREATE SET d.isopump_load_initial = timestamp()
                        ON MATCH SET d.isopump_load_last = timestamp()
                        MERGE (d)-[:{source_label}]->(s)
                        """.format(**{
                            "neo_label": "Dolphin",
                            "doc_id": document_id,
                            "doc_label": "Document",
                            "source_label": "Source",
                            "peripheral_id": dolphin
                        })
            execute_cypher(cypher)       
    logger.debug('New dolphin and document nodes created')

def mark_fully_loaded(label):
    # Mark central node as fully loaded
    logger.debug('Marking {0} as fully loaded'.format(label))
    cypher = """MERGE (s:{neo_label} {{ id: '{doc_id}'}})
                    SET s.isopump_fully_loaded = TRUE
                    """.format(**{
                        "neo_label": "Dolphin",
                        "doc_id": label
                    })
    execute_cypher(cypher)


def seed_neo_graph(query_label):
    logger.debug("Seeding neo graph with elasticsearch {0}".format(query_label))
    hits = dolphin_label_hits(query_label)
    merge_hits_to_node(hits)
    mark_fully_loaded(query_label)

class SearchDolphins(SmartResource):
    '''Get raw search results'''

    def get(self):
        '''
        Return the elastic results of a document search using query parameters.

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json

            [
                {
                    "_index": "dolphins",
                    "_source": {
                        "dolphins": [
                            "Zap",
                            "CCL"
                        ]
                    },
                    "_id": "AVrDasjxocluSgWq6vsT",
                    "_type": "dolphin_sighting",
                    "_score": 2.6732156
                },
                {
                    "_index": "dolphins",
                    "_source": {
                        "dolphins": [
                            "Zap",
                            "Double"
                        ]
                    },
                    "_id": "AVrDasj8ocluSgWq6vsU",
                    "_type": "dolphin_sighting",
                    "_score": 2.6732156
                }
            ]

        :query string label: id of dolphin to search documents for
        :statuscode 200: OK
        '''
        self.logger.debug('Searching dolphins')
        query_id = request.args.get('id', '')
        query_label = request.args.get('label', '')

        results = dolphin_label_hits(query_label)            
        return results, 200


class SeedGraph(SmartResource):
    '''Seed a single entity in the graph from document store'''

    def get(self):
        '''
        Seed a node (and mentioning documents) from elastic to neo,
        and return the node id

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 201 CREATED
            Content-Type: application/json
            
            {
                "id": "Zap"
            }

        :query string label: id of dolphin to search documents for
        :statuscode 201: Created graph node(s)
        '''
        self.logger.debug('Seeding graph')
        query_label = request.args.get('label', '')
        seed_neo_graph(query_label)
        return {"id": query_label}, 201

