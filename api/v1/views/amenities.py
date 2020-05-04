#!/usr/bin/python3
"""This module create view for City objects
   that handles all default RestFul API actions
"""

# from models import storage
# from models.state import State

from api.v1.views import storage, Amenity, app_views
from flask import jsonify, abort, request


@app_views.route("/amenities", methods=["GET"])
def get_amenities():
    """  list of all Amenity objects """

    all_amenities = [state.to_dict()
                     for state in storage.all(Amenity).values()]

    return jsonify(all_amenities)


@app_views.route("/amenities/<amenity_id>", methods=["GET"])
def get_amenity_by_name(amenity_id=None):
    """ display a resource of my list of amenities """

    amenity_object = storage.get(Amenity, amenity_id)
    if amenity_object is None:
        abort(404, "Not found")

    return jsonify(amenity_object.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"])
def delete_amenity(amenity_id=None):
    """ delete a resource of my list of states """

    amenity_object = storage.get(Amenity, amenity_id)
    if amenity_object is None:
        abort(404, "Not found")

    storage.delete(amenity_object)
    storage.save()

    return jsonify("{}"), 200


@app_views.route("/amenities", methods=["POST"])
def create_new_amenity(state_id=None):
    """ create new resource by my list of amenities """

    amenity_object_json = request.get_json()
    if amenity_object_json is None:
        abort(400, "Not a JSON")

    if 'name' not in amenity_object_json.keys():
        abort(400, "Missing name")

    amenity_object = Amenity(**amenity_object_json)
    amenity_object.save()

    return jsonify(amenity_object.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"])
def update_a_amenity(amenity_id=None):
    """ update a resource of my objects """

    amenity_object_json = request.get_json()
    if amenity_object_json is None:
        abort(400, "Not a JSON")

    amenity_object = storage.get(Amenity, amenity_id)
    if amenity_object is None:
        abort(404, "Not found")

    amenity_object.update(amenity_object_json)

    return jsonify(amenity_object.to_dict()), 200
