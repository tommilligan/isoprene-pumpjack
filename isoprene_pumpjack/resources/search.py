#!/usr/bin/env python
'''
Provide a JSON serialized set of search results.
'''

from flask import request
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q, Index, DocType, Text, Nested, InnerObjectWrapper

import isoprene_pumpjack.utils as utils


i = Index('dolphins')

@i.doc_type
class Dolphin(DocType):
    id = Text()
    label = Text()

@i.doc_type
class DolphinSighting(DocType):
    dolphins = Text()


class SearchDolphins(utils.SmartResource):
    '''API endpoint to provide config JSON for synaptic-scout'''

    def get(self):
        '''Get documents containinga single dolphin by id and label'''
        self.logger.debug('Searching')
        query_id = request.args.get('id', '')
        query_label = request.args.get('label', '')

        q = Q('match', dolphins=query_label)
        s = Search().query(q).index('dolphins').doc_type(DolphinSighting)
        self.logger.debug('Executing elastic search {0}'.format(s.to_dict()))
        response = s.execute()
        self.logger.debug('Search found {0} results'.format(response.hits.total))
        results = response.hits.hits

        return results, 200

