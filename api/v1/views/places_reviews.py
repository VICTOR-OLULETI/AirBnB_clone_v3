#!/usr/bin/python3
""" This script defines methods for the REST api for Review object"""
from flask import jsonify, request, make_response, abort
from api.v1.views import app_views
from models import storage
#from models.place import Place
#from models.city import City
from models.reviews import Review


@app_views.route(
        '/places/<place_id>/reviews', methods=['GET', 'POST'],
        strict_slashes=False)
def review_1(place_id=None):
    """ This function retrieves all the list of Review objects """
    resp = storage.all("Review")
    resp2 = storage.get('Place', place_id)
    if resp2 is None:
        abort(404, {'error': 'Not found'})
    # resp1 = [i.to_dict() for i in resp.values() if i.place_id == place_id]
    resp1 = [i.to_dict() for i in resp2.reviews]
    if request.method == 'GET':
        if resp1 is None:
            """ if response is none """
            abort(404, {'error': 'Not found'})
        return jsonify(resp1)

    if request.method == 'POST':
        resp = request.get_json()
        if not resp:
            """ if response is none """
            abort(400, {'error': 'Not a JSON'})

        if resp.get('text') is None:
            abort(400, {'error': 'Missing text'})
        if resp.get('user_id') is None:
            abort(400, {'error': 'Missing user_id'})
        user_id = resp.get('user_id')
        resp3 = storage.get("User", user_id)
        if not resp3:
            """ if response is none """
            abort(404, {'error': 'Not found'})
        resp['place_id'] = place_id
        new_review = Review(**resp)
        new_review.save()
        return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route(
        '/reviews/<string:review_id>', methods=['GET', 'DELETE', 'PUT'],
        strict_slashes=False)
def review_2(review_id=None):
    """ This function returns the status of the api """
    resp = storage.get('Review', review_id)
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
                    'place_id',
                    'created_at',
                    'updated_at']:
                setattr(resp, key, value)
        resp.save()
        return make_response(jsonify(resp.to_dict()), 200)
