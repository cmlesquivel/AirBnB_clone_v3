#!/usr/bin/python3
"""This module create view for City objects
   that handles all default RestFul API actions
"""

# from models import storage
# from models.state import State

from api.v1.views import storage, City, Place, User, app_views
from flask import jsonify, abort, request


@app_views.route("/cities/<city_id>/places", methods=["GET"])
def get_places_by_city_id(city_id=None):
    """  list of all places objects of a city """

    city = storage.get(City, city_id)
    if city is None:
        abort(404, "Not found")

    all_places = [iplace.to_dict() for iplace in city.places]

    return jsonify(all_places)


@app_views.route("/places/<place_id>", methods=["GET"])
def get_place_by_id(place_id=None):
    """ display a resource of my list of places """

    place_object = storage.get(Place, place_id)
    if place_object is None:
        abort(404, "Not found")

    return jsonify(place_object.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"])
def delete_place_by_id(place_id=None):
    """ delete a resource of my list of states """

    place_object = storage.get(Place, place_id)
    if place_object is None:
        abort(404, "Not found")

    storage.delete(place_object)
    storage.save()

    return jsonify("{}"), 200


@app_views.route("/cities/<city_id>/places", methods=["POST"])
def create_new_place(city_id=None):
    """ create new resource by my list of places """

    city_object = storage.get(City, city_id)
    if city_object is None:
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
    if place_object_json.get("name") is None:
        abort(400, 'Missing name')

    # If the city_id is not linked to any City object, raise a 404 error
    # this will be never raise a 404 error
    place_object_json["city_id"] = city_id

    place_object = Place(**place_object_json)
    place_object.save()

    return jsonify(place_object.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"])
def update_a_place_by_id(place_id=None):
    """ update a resource of my objects """

    place_object_json = request.get_json()
    if place_object_json is None:
        abort(400, "Not a JSON")

    place_object = storage.get(Place, place_id)
    if place_object is None:
        abort(404, "Not found")

    place_object.update(place_object_json)

    return jsonify(place_object.to_dict()), 200
