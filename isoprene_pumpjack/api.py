#!/usr/bin/env python
'''Provide the isoprene_pumpjack Flask application object as `app`'''

import logging

from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from isoprene_pumpjack.resources.synaptic_scout_config import SynapticScoutConfig


# Define Flask app
app = Flask(__name__)
cors = CORS(app)
api = Api(app)


# Add resources
api.add_resource(SynapticScoutConfig, '/configuration/synaptic-scout')


def main():
    '''Run isoprene_pumpjack using the Flask dev server'''
    # Setup logging
    logger = logging.getLogger('isoprene_pumpjack')
    logger.setLevel(logging.DEBUG)
    stream = logging.StreamHandler()
    stream.setFormatter(logging.Formatter('%(asctime)s|%(name)s|%(levelname)s|%(message)s'))
    stream.setLevel(logging.DEBUG)
    logger.addHandler(stream)

    # If called as script, start flask dev server
    app.run(debug=True)


if __name__ == '__main__':
    main()
