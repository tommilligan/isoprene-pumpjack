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

from flask_restful import Resource
from neo4j.v1 import GraphDatabase, basic_auth

import isoprene_pumpjack.constants.environment as ip_env
import isoprene_pumpjack.utils as utils
from isoprene_pumpjack.utils.dolphins import dolphins


driver = GraphDatabase.driver(
    ip_env.ISOPRENE_PUMPJACK_BOLT_URL,
    auth=basic_auth(
        ip_env.ISOPRENE_PUMPJACK_BOLT_USER,
        ip_env.ISOPRENE_PUMPJACK_BOLT_PASSWORD
    )
)


def set_graph(data):
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")

        for node in data["nodes"]:
            session.run("CREATE (a:Dolphin {id: {id}, label: {label}})",
                        node)

        for link in data["links"]:
            session.run("""MATCH (s:Dolphin {id: {source}}), (t:Dolphin {id: {target}})
                        CREATE (s)-[:knows]->(t)""",
                        link)

def neo_node_to_d3_node(node):
    d3node = {
        "id": node.id,
        "labels": [label for label in node.labels],
        "props": {k: v for k, v in node.items()}
    }
    return d3node

def neo_link_to_d3_link(link):
    d3link = {
        "id": link.id,
        "source": link.start,
        "target": link.end,
        "labels": [link.type],
        "props": {k: v for k, v in link.items()}
    }
    return d3link

def neo_result_to_d3_result(result, nodeLabels, linkLabels):
    '''Convert a set of neo results to a drawable nodes/links dictionary
    
    Takes
    * the neo result (BoltStatementResult)
    * a list of node labels (string[])
    * a list of link labels (string[])

    Dedupes to the standard format:
    {
        nodes: [
            {
                id: string,
                labels: string[],
                properties: {}
            }
        ],
        links: [
            {
                id: string,
                source: string,
                target: string,
                type: string
                properties: {}
            }
        ]
    }
    '''
    d3data = {
        "nodes": [],
        "links": []
    }

    process_neo_objects = [
        {
            "labels": nodeLabels,
            "function": neo_node_to_d3_node,
            "d3key": "nodes"
        },
        {
            "labels": linkLabels,
            "function": neo_link_to_d3_link,
            "d3key": "links"
        }
    ]

    for record in result:
        for process in process_neo_objects:
            for label in process["labels"]:
                neo_objects = record[label]
                if isinstance(neo_objects, list):
                    for neo_object in neo_objects:
                        d3object = process["function"](neo_object)
                        d3data[process["d3key"]].append(d3object)
                else:
                    neo_object = neo_objects
                    d3object = process["function"](neo_object)
                    d3data[process["d3key"]].append(d3object)
    
    d3data["nodes"] = utils.dedupe_dict_list(d3data["nodes"], "id")
    d3data["links"] = utils.dedupe_dict_list(d3data["links"], "id")

    return d3data


def get_full_graph():
    '''Transparently pass all database data'''
    with driver.session() as session:
        result = session.run("""MATCH (d)-[r]-()
                        RETURN d, r""")
    
    data = neo_result_to_d3_result(result, ["d"], ["r"])
    return data

def get_sub_graph(central_node_id):
    '''Quick and dirty subgraph - throw away most nodes and corresponding links
    '''
    with driver.session() as session:
        result = session.run("""MATCH (s)-[r*1..2]-(t)
                        WHERE s.id = {id}
                        RETURN s, r, t""",
                        {"id": central_node_id})
    
    data = neo_result_to_d3_result(result, ["s", "t"], ["r"])
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


class ResetDolphins(Resource):
    '''Debug endpoint - reset neo4j'''
    def __init__(self):
        self.logger = utils.object_logger(self)

    def get(self):
        '''Drop database and upload dolphins JSON data into Neo4j'''
        self.logger.debug('Resetting neo4j to dolphins')
        set_graph(dolphins)
        return {}, 200


class FullGraph(Resource):
    '''Provide all graph data from backend'''
    def __init__(self):
        self.logger = utils.object_logger(self)

    def get(self):
        '''Get JSON representing full graph'''
        self.logger.debug('Getting full graph')
        full_graph = get_full_graph()
        return full_graph, 200
