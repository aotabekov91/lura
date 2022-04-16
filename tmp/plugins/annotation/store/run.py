#!/usr/bin/env python
"""
run.py: A simple example app for using the Annotator Store blueprint

This file creates and runs a Flask[1] application which mounts the Annotator
Store blueprint at its root. It demonstrates how the major components of the
Annotator Store (namely the 'store' blueprint, the annotation model and the
auth and authz helper modules) fit together, but it is emphatically NOT
INTENDED FOR PRODUCTION USE.

[1]: http://flask.pocoo.org
"""

import os
import sys

from flask import Flask, g, current_app
from lura.plugins.annotation.store.store import store

from flask_cors import CORS, cross_origin

def main(argv):

    app = Flask(__name__)

    cfg_file = 'annotator.cfg'

    cfg_path = os.path.join(os.path.dirname(__file__), cfg_file)

    app.config.from_pyfile(cfg_path)

    app.register_blueprint(store)

    host = os.environ.get('HOST', '127.0.0.1')
    port = int(os.environ.get('PORT', 5000))
    app.run(host=host, port=port)

if __name__ == '__main__':
    try:
        main(sys.argv)
    except:
        pass
