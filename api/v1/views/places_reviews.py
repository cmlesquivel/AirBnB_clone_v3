#!/usr/bin/python3
"""This module create view for City objects
   that handles all default RestFul API actions
"""

# from models import storage
# from models.state import State

from api.v1.views import storage, Place, Review, User, app_views
from flask import jsonify, abort, request


@app_views.route("/places/<place_id>/reviews", methods=["GET"])
def get_review_by_place_id(place_id=None):
    """  list of all places objects of a review """

    place = storage.get(Place, place_id)
    if place is None:
        abort(404, "Not found")

    all_reviews = [ireview.to_dict() for ireview in place.reviews]

    return jsonify(all_reviews)


@app_views.route("/reviews/<review_id>", methods=["GET"])
def get_review_by_id(review_id=None):
    """ display a resource of my list of reviews """

    review_object = storage.get(Review, review_id)
    if review_object is None:
        abort(404, "Not found")

    return jsonify(review_object.to_dict())


@app_views.route("/reviews/<review_id>", methods=["DELETE"])
def delete_review_by_id(review_id=None):
    """ delete a resource of my list of review """

    review_object = storage.get(Review, review_id)
    if review_object is None:
        abort(404, "Not found")

    storage.delete(review_object)
    storage.save()

    return jsonify("{}"), 200


@app_views.route("/places/<place_id>/reviews", methods=["POST"])
def create_new_review(place_id=None):
    """ create new resource by my list of reviews """

    place_object = storage.get(Place, place_id)
    if place_object is None:
        abort(404, "Not found")

    place_object_json = request.get_json()
    if place_object_json is None:
        abort(400, "Not a JSON")

    # looking for a "user_id" value for creating a object place
    user_id = place_object_json.get("user_id")
    if user_id is None:
        abort(400, 'Missing user_id')

    # creating a new user object as attribute of place object
    user_object = storage.get(User, user_id)
    if user_object is None:
        abort(404, "Not found")

    # verify if exist "name" value into POST request
    if place_object_json.get("text") is None:
        abort(400, 'Missing text')

    # If the place_id is not linked to any City object, raise a 404 error
    # this will be never raise a 404 error
    place_object_json["place_id"] = place_id

    review_object = Review(**place_object_json)
    review_object.save()

    return jsonify(review_object.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"])
def update_a_review_by_id(review_id=None):
    """ update a resource of my objects """

    review_object_json = request.get_json()
    if review_object_json is None:
        abort(400, "Not a JSON")

    review_object = storage.get(Review, review_id)
    if review_object is None:
        abort(404, "Not found")

    review_object.update(review_object_json)

    return jsonify(review_object.to_dict()), 200
