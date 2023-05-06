#!/usr/bin/python3
""" This script defines methods for the api """
from flask import jsonify, request
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'])
def state():
    """ This function returns the status of the api """
    if request.method == 'GET':
        response = {"status": "OK"}
        return jsonify(response)


@app_views.route('/stats', methods=['GET'])
def stats():
    """ This function returns the number of objects of each table """
    if request.method == 'GET':
        my_dict = {}
        temp_dict = {
                "amenities": "Amenity",
                "cities": "City",
                "places": "Place",
                "reviews": "Review",
                "states": "State",
                "users": "User"
                }
        for key, value in temp_dict.items():
            my_dict[key] = storage.count(value)
        resp = jsonify(my_dict)
        return resp
