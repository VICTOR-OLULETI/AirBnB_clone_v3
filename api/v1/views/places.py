#!/usr/bin/python3
""" This script defines methods for the api """
from flask import jsonify, request, make_response, abort
from api.v1.views import app_views
from models import storage
from models.places import Place
from models.cities import City


@app_views.route(
        '/cities/<city_id>/places', methods=['GET', 'POST'],
        strict_slashes=False)
def place_1(city_id=None):
    """This function retrieves all the list of city objects """
    resp = storage.all("Place")
    resp2 = storage.get('City', city_id)
    if resp2 is None:
        abort(404, {'error': 'Not found'})
    # resp1 = [i.to_dict() for i in resp.values() if i.city_id == city_id]
    resp1 = [i.to_dict() for i in resp2.places]
    if request.method == 'GET':
        if resp1 is None:
            abort(404, {'error': 'Not found'})
        return jsonify(resp1)

    if request.method == 'POST':
        resp = request.get_json()
        if not resp:
            """ if response is none """
            abort(400, {'error': 'Not a JSON'})

        if resp.get('name') is None:
            abort(400, {'error': 'Missing name'})
        if resp.get('user_id') is None:
            abort(400, {'error': 'Missing user_id'})
        user_id = resp.get('user_id')
        resp3 = storage.get("User", user_id)
        if not resp3:
            abort(404, {'error': 'Not found'})
        resp['city_id'] = city_id
        new_place = Place(**resp)
        new_place.save()
        return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route(
        '/places/<string:place_id>', methods=['GET', 'DELETE', 'PUT'],
        strict_slashes=False)
def place_2(place_id=None):
    """ This function returns the status of the api """
    resp = storage.get('Place', place_id)
    if resp is None:
        abort(404, {'error': 'Not found'})
    if request.method == 'GET':
        return jsonify(resp.to_dict())

    if request.method == 'DELETE':
        resp.delete()
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        data = request.get_json()
        if data is None:
            """ if data is none """
            abort(400, {'error': 'Not a JSON'})

        for key, value in data.items():
            if key not in [
                    'id',
                    'user_id',
                    'city_id',
                    'created_at',
                    'updated_at']:
                setattr(resp, key, value)
        resp.save()
        return make_response(jsonify(resp.to_dict()), 200)
