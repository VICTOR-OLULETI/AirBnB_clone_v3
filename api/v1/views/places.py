#!/usr/bin/python3
""" This script defines methods for the api """
from flask import jsonify, request, make_response, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City


@app_views.route(
                '/places_search',
                methods=['POST'],
                strict_slashes=False)
def place_search():
    """ This function retrieves all Place objects depending on the
    JSON in the body of the request.
    The JSON contains 3 optional keys:
        states: list of state ids
        cities: list of City ids
        amenities: list of Amenity ids
    """
    if request.method == 'POST':
        data = request.get_json()
        place = []
        Place = storage.all('Place')
        all_places = [i.to_dict() for i in Place.values()]
        if data is None:
            """ if data is none """
            abort(400, {'error': 'Not a JSON'})
        if not data or len(data) == 0:
            return(jsonify(all_places))
        states = data.get('states')
        amenity_ids = data.get('amenities')
        cities = data.get('cities')
        if states is None and amenity_ids is None and cities is None:
            return (jsonify(all_places))
        if states:
            """ list of states """
            list_of_states = [
                    storage.get('State', state_id) for state_id in states]
            """ list of cities in states """
            list_of_cities = [
                city for state in list_of_states for city in state.cities]
            # print(list_of_cities)
            """ list of places in cities """
            list_of_places = [c.places for c in list_of_cities]
            place.extend(list_of_places)
        if cities:
            list_of_cities = [
                storage.get('City', city_id) for city_id in cities]
            print(list_of_cities)
            list_of_places = [
                city.places for city in list_of_cities if city is not None]
            place.extend(list_of_places)
        if amenity_ids:
            list_of_amenities = [
                storage.get("Amenity", amenity_id)
                for amenity_id in amenity_ids]
            if place is not None:
                list_of_places_1 = [
                    p for p in place if all(
                        item in p.amenities for item in list_of_amenities
                        )]
            else:
                list_of_places_1 = [
                    p for p in Place if all(
                        item in p.amenities for item in list_of_amenities)]
            place = list_of_places_1
        resp1 = [i for j in place for i in j]
        resp1 = list(set(resp1))
        # resp = [i.to_dict() for p in place for i in p]
        resp = [i.to_dict() for i in resp1]
        # print(resp)
        return (jsonify(resp))


@app_views.route(
        '/cities/<city_id>/places', methods=['GET', 'POST'],
        strict_slashes=False)
def place_1(city_id=None):
    """ This function retrieves all the list of city objects """
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
