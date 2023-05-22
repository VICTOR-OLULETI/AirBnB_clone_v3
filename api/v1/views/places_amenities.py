#!/usr/bin/python3
"""
    This script defines methods for the REST api for Review object.
    It performs the following methods: get, post, delete, put.
"""
from flask import jsonify, request, make_response, abort
from api.v1.views import app_views
from models import storage
from os import environ
from models.review import Review


@app_views.route(
        '/places/<string:place_id>/amenities', methods=['GET'],
        strict_slashes=False)
def place_amenities_1(place_id=None):
    """ This function retrieves all the list of Review objects """
    # resp = storage.all("Review")
    place = storage.get('Place', place_id)
    if place is None:
        abort(404, {'error': 'Not found'})
    # resp1 = [i.to_dict() for i in resp.values() if i.place_id == place_id]
    if environ.get('HBNB_TYPE_STORAGE') == "db":
        resp1 = [amty.to_dict() for amty in place.amenities]
    else:
        resp1 = [
            storage.get('Amenity', amty_id) for amty_id in place.amenity_ids
            ]
    if request.method == 'GET':
        if resp1 is None:
            """ if response is none """
            abort(404, {'error': 'Not found'})
        return jsonify(resp1)


@app_views.route(
        '/places/<string:place_id>/amenities/<string:amenity_id>',
        methods=['POST', 'DELETE'],
        strict_slashes=False)
def place_amenities_2(place_id=None, amenity_id=None):
    """ This function returns the status of the api """
    place = storage.get('Place', place_id)
    amenity = storage.get('Amenity', amenity_id)
    # resp3 = [amt_id for amt_id in place.amenity_ids if amt_id == amenity_ids]
    if place is None:
        abort(404, {'error': 'Not found'})
    if amenity is None:
        abort(404, {'error': 'Not found'})

    if request.method == 'DELETE':
        if environ.get('HBNB_TYPE_STORAGE') == "db":
            if amenity not in place.amenities:
                abort(404, {'error': 'Not found'})
            place.amenities.remove(amenity)
        else:
            if amenity_id not in place.amenity_ids:
                abort(404, {'error': 'Not found'})
            place.amenity_ids.remove(amenity_id)
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'POST':
        # resp = request.get_json()
        # if not resp:
        #    """ if response is none """
        #    abort(400, {'error': 'Not a JSON'})
        if environ.get('HBNB_TYPE_STORAGE') == "db":
            if amenity in place.amenities:
                """ if amenity is not in the place object """
                return make_response(jsonify(amenity.to_dict()), 200)
            else:
                place.amenities.append(amenity)
        else:
            if amenity_id in place.amenity_ids:
                """ if the amenity id is not in the previously stored ids
                    in the place object
                """
                return make_response(jsonify(amenity.to_dict()), 200)
            else:
                place.amenity_ids.append(amenity_id)
        storage.save()
        return make_response(jsonify(amenity.to_dict()), 201)
