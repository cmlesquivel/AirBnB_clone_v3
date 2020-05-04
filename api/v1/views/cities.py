#!/usr/bin/python3
"""This module create view for City objects
   that handles all default RestFul API actions
"""

# from models import storage
# from models.state import State

from api.v1.views import storage, State, City, app_views
from flask import jsonify, abort, request


@app_views.route("/states/<state_id>/cities", methods=["GET"])
def get_cities(state_id=None):
    """  list of all City objects of a State """

    state = storage.get(State, state_id)
    if state is None:
        abort(404, "Not found")

    all_cities = [icity.to_dict() for icity in state.cities]

    return jsonify(all_cities)


@app_views.route("/cities/<city_id>", methods=["GET"])
def get_cities_by_name(city_id=None):
    """ display a resource of my list of states """

    city_object = storage.get(City, city_id)
    if city_object is None:
        abort(404, "Not found")

    return jsonify(city_object.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"])
def delete_city(city_id=None):
    """ delete a resource of my list of states """

    city_object = storage.get(City, city_id)
    if city_object is None:
        abort(404, "Not found")

    storage.delete(city_object)
    storage.save()

    return jsonify("{}"), 200


@app_views.route("/states/<state_id>/cities", methods=["POST"])
def create_new_city(state_id=None):
    """ create new resource by my list of cities """

    state_object = storage.get(State, state_id)
    if state_object is None:
        abort(400, "Not found")

    city_object_json = request.get_json()
    if city_object_json is None:
        abort(400, "Not a JSON")

    if 'name' not in city_object_json.keys():
        abort(400, "Missing name")

    # If the state_id is not linked to any State object, raise a 404 error
    # this will be never raise a 404 error
    city_object_json["state_id"] = state_id
    object_city = City(**city_object_json)
    object_city.save()

    return jsonify(object_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"])
def update_a_city(city_id=None):
    """ update a resource of my objects """

    city_object_json = request.get_json()
    if city_object_json is None:
        abort(400, "Not a JSON")

    city_object = storage.get(City, city_id)
    if city_object is None:
        abort(404, "Not found")

    city_object.update(city_object_json)

    return jsonify(city_object.to_dict()), 200
