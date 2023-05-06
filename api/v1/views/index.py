#!/usr/bin/python3
from flask import jsonify, request
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def state():
    """ This function returns the status of the api """
    if request.method == 'GET':
        response = {"status": "OK"}
        return jsonify(response)
