#!/usr/bin/python3
""" This script defines methods for the api """
from flask import jsonify, request, make_response, abort
from api.v1.views import app_views
from models import storage
from models.places import Place
from models.cities import City


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'])
def city_1(city_id=None):
    """This function retrieves all the list of city objects """
    resp = storage.all("City")
    resp1 = [i.to_dict() for i in resp.values() if i.city_id == city_id]
    resp2 = storage.get("City", city_id)
    if request.method == 'GET':
        if resp1 is None:
            abort(404, {'error': 'Not found'})
        return jsonify(resp1)

    if request.method == 'POST':
        resp = request.get_json()
        if not resp2:
            abort(404, {'error': 'Not found'})
        if not resp:
            """ if response is none """
            abort(400, {'error': 'Not a JSON'})

        # if resp1 is None:
        #    abort(404, {'error': 'Not found'})

        if resp.get('name') is None:
            abort(400, {'error': 'Missing name'})
        if resp.get('user_id') is None:
            abort(400, {'error': 'Missing user_id'})
        # State = classes.get('State')
        user_id = resp.get('user_id')
        resp3 = storage.get("User", user_id)
        if not resp3:
            abort(404, {'error': 'Not found'})
        new_city = City(**resp)
        new_city.save()
        return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'])
def city_2(place_id=None):
    """ This function returns the status of the api """
    resp = storage.get('Place', place_id)
    if request.method == 'GET':
        # resp = storage.get(State, state_id)
        if resp is None:
            abort(404, 'Not found')

        return jsonify(resp.to_dict())

    if request.method == 'DELETE':
        if resp is None:
            abort(404, 'Not found')
        else:
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
