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
from isoprene_pumpjack.utils.neo_to_d3 import neo_to_d3
from isoprene_pumpjack.constants.environment import bolt_driver

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
    q = Q('match', dolphins=label)
    s = Search().query(q).index('dolphins').doc_type(DolphinSighting)
    logger.debug('Executing elastic search {0}'.format(s.to_dict()))
    response = s.execute()
    logger.debug('Search found {0} results'.format(response.hits.total))
    return response.hits.hits

def merge_hits_to_node(hits, label):
    '''Collate document records to nodes and links, and upload to neo'''
    logger.debug('Merging {0} elastic documents to neo node'.format(len(hits)))

    document_ids = json.dumps([hit["_id"] for hit in hits])
    with bolt_driver.session() as session:
        result = session.run("""MERGE (d:{neo_label} {{ label: '{data_label}', id: '{data_label}' }})
                        ON CREATE SET d.isopump_load_initial = timestamp()
                        ON MATCH SET d.isopump_load_last = timestamp()
                        RETURN d
                        """.format(**{
                            "neo_label": "Dolphin",
                            "data_label": label,
                            "document_ids": document_ids
                        }))
        created = neo_to_d3(result, ["d"])
        created_id = created["nodes"][0]["props"]["id"]
        logger.debug('New dolphin node created with id {0}'.format(created_id))

        for document in hits:
            session.run("""MATCH (c:{central_label} {{ id: '{central_id}' }})
                        MERGE (d:{neo_label} {{ id: '{doc_id}' }})
                        ON CREATE SET d.isopump_load_initial = timestamp()
                        ON MATCH SET d.isopump_load_last = timestamp()
                        MERGE (c)-[:{doc_label}]->(d)
                        """.format(**{
                            "central_id": created_id,
                            "doc_label": "Source",
                            "central_label": "Dolphin",
                            "neo_label": "Document",
                            "doc_id": document["_id"]
                        }))
            logger.debug('New document node created')

    return created_id

class SearchDolphins(SmartResource):
    '''API endpoint to provide config JSON for synaptic-scout'''

    def get(self):
        '''Get documents containinga single dolphin by id and label'''
        self.logger.debug('Searching dolphins')
        query_id = request.args.get('id', '')
        query_label = request.args.get('label', '')

        results = dolphin_label_hits(query_label)
        return results, 200


class SeedGraph(SmartResource):
    '''Seed a node from elastic to neo and return the node id'''

    def get(self):
        '''Get documents containing a single dolphin by id and label'''
        self.logger.debug('Seeding graph')
        query_label = request.args.get('label', '')

        hits = dolphin_label_hits(query_label)
        central_node_id = merge_hits_to_node(hits, query_label)

        return {"id": central_node_id}, 201

