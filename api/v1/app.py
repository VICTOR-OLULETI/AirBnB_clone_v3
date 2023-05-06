#!/usr/bin/python3
""" This script checks the status of the API """
from flask import Flask
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)
# get the value of HBNB_API_HOST environment variable or use default 0.0.0.0
host = os.getenv('HBNB_API_HOST', '0.0.0.0')
# get the value of HBNB_API_PORT' environment variable or use default 5000
port = os.getenv('HBNB_API_PORT', 5000)


@app.teardown_appcontext
def cleanup(exception):
    """ Closes down the storage session """
    storage.close()


if __name__ == "__main__":
    """ start Flask app """
    app.run(host=host, port=port, threaded=True)
