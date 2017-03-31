.. _neo-d3-json:

Neo-D3-JSON
===========

Data is often returned from isoprene-pumpjack to instruct synpatic-scout how to draw a graph.

This is done in a standard JSON format, described below:


Neo-D3-JSON Specification
^^^^^^^^^^^^^^^^^^^^^^^^^

Nodes & Links
-------------

The object contains an array of **nodes** and an array of **links**.
This is a naming convention taken from d3 force-constrained graphs:

.. sourcecode:: http

    HTTP/1.1 200 OK
    Content-Type: application/json

    {
        "nodes": [],
        "links": []
    }



The response from Neo is deduplicated, so each node and link is unique.

Both nodes and links have the following standard properties::

    {
        "labels": string[],    # Array of Neo labels
        "id": any,             # Neo internal id (not reccomended for external use)
        "props": {},           # Object containg any additional properties
        ...
    }

Nodes
-----

``Node`` objects have no additional properties.

Links
-----

``Link`` objects also contain the following properties::

    {
        "target": any,         # Target of link
        "source": any,         # Source of link
        ...
    }

``source`` and ``target`` will match the ``id`` property of a ``node`` object.

All links are considered directed by neo - it is up to the UI to render nondirected
links if required.

Please note: unlike Neo, link labels are represented as an array of length 1,
in order to be consistent with node properties.


.. _neo-d3-json-example:

Neo-D3-JSON Example Response
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. sourcecode:: http

    HTTP/1.1 200 OK
    Content-Type: application/json
    
    {  
        "nodes":[  
            {  
                "labels":[  
                    "Document"
                ],
                "id":0,
                "props":{  
                    "isopump_fully_loaded":true,
                    "label":"AVrDasjxocluSgWq6vsT",
                    "isopump_load_last":1490949576577,
                    "id":"AVrDasjxocluSgWq6vsT",
                    "isopump_load_initial":1490714160644
                }
            },
            {  
                "labels":[  
                    "Dolphin"
                ],
                "id":1,
                "props":{  
                    "isopump_fully_loaded":true,
                    "id":"Zap",
                    "label":"Zap",
                    "isopump_load_last":1490949577244,
                    "isopump_load_initial":1490714160644
                }
            }
        ],
        "links":[  
            {  
                "props":{  

                },
                "labels":[  
                    "Source"
                ],
                "id":0,
                "target":0,
                "source":1
            }
        ]
    }
