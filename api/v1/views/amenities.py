#!/usr/bin/python3
""" This script defines methods for the api """
from flask import jsonify, request, make_response, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET', 'POST'])
# @app_views.route('/states/', methods=['GET', 'POST'])
def amenity_1():
    """This function retrieves all the list of state objects """
    if request.method == 'GET':
        resp = storage.all("Amenity")
        resp1 = [i.to_dict() for i in resp.values()]
        return jsonify(resp1)

    if request.method == 'POST':
        resp = request.get_json()
        if not resp:
            """ if response is none """
            abort(400, {'error': 'Not a JSON'})

        if resp.get('name') is None:
            abort(400, {'error': 'Missing name'})
        new_amenity = Amenity(**resp)
        new_amenity.save()
        return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'])
def amenity_2(amenity_id=None):
    """ This function returns the status of the api """
    resp = storage.get('Amenity', amenity_id)
    if request.method == 'GET':
        if resp is None:
            abort(404, 'Not found')

        return jsonify(resp.to_dict())

    if request.method == 'DELETE':
        if resp is None:
            abort(404, 'Not found')
        else:
            # resp.delete()
            # storage.all('State').pop(resp)
            storage.delete(resp)
            storage.save()
            del resp
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        if resp is None:
            abort(404, 'Not found')
        data = request.get_json()
        if data is None:
            abort(400, 'Not a JSON')

        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(resp, key, value)
        # obj = resp(**data)
        resp.save()
        return make_response(jsonify(resp.to_dict()), 200)
