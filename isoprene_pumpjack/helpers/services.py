#!/usr/bin/env python
'''
Central execution points for non-python services
'''

import logging

from isoprene_pumpjack.constants.environment import bolt_driver
from isoprene_pumpjack.utils.neo_to_d3 import neo_to_d3
from isoprene_pumpjack.exceptions import GraphServiceException, DocumentServiceException

logger = logging.getLogger(__name__)

# TODO - some error handling here?
def execute_cypher(cypher_statement):
    logger.debug("Executing cypher statement")
    with bolt_driver.session() as session:
        result = session.run(cypher_statement)
    return result

def execute_cypher_get_d3(cypher_statement, nodeLabels=[], linkLabels=[]):
    logger.debug("Executing cypher and returning as d3 dict")
    result = execute_cypher(cypher_statement)
    data = neo_to_d3(result, nodeLabels, linkLabels)
    return data
