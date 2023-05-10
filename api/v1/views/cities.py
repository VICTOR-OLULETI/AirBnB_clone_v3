#!/usr/bin/python3
""" This script defines methods for the api """
from flask import jsonify, request, make_response, abort
from api.v1.views import app_views
from models import storage
from models.city import City


@app_views.route(
        '/states/<string:state_id>/cities', methods=['GET', 'POST'],
        strict_slashes=False)
def city_1(state_id=None):
    """This function retrieves all the list of state objects """
    resp = storage.all("City")
    resp2 = storage.get("State", state_id)
    if resp2 is None:
        abort(404, {'error': 'Not found'})
    resp1 = [i.to_dict() for i in resp2.cities]
    # or resp1 = [i.to_dict() for i in resp.values() if i.state_id == state_id
    if request.method == 'GET':
        if resp2 is None:
            abort(404, {'error': 'Not found'})
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
        # State = classes.get('State')
        new_state = City(**resp)
        new_state.save()
        return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route(
        '/cities/<string:city_id>', methods=['GET', 'DELETE', 'PUT'],
        strict_slashes=False)
def city_2(city_id=None):
    """ This function returns the status of the api """
    resp = storage.get('City', city_id)
    if resp is None:
        abort(404, 'Not found')
    if request.method == 'GET':
        return jsonify(resp.to_dict())

    if request.method == 'DELETE':
        resp.delete()
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        data = request.get_json()
        if data is None:
            abort(400, 'Not a JSON')

        for key, value in data.items():
            if key not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(resp, key, value)
        resp.save()
        return make_response(jsonify(resp.to_dict()), 200)
