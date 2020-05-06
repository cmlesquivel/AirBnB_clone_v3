#!/usr/bin/python3
"""This module create view for City objects
   that handles all default RestFul API actions
"""

# from models import storage
# from models.state import State

from api.v1.views import storage, User, app_views
from flask import jsonify, abort, request


@app_views.route("/users", methods=["GET"])
def get_users():
    """  list of all users objects """

    all_users = [user.to_dict()
                 for user in storage.all(User).values()]

    return jsonify(all_users)


@app_views.route("/users/<user_id>", methods=["GET"])
def get_user_by_name(user_id=None):
    """ display a resource of my list of users """

    user_object = storage.get(User, user_id)
    if user_object is None:
        abort(404, "Not found")

    return jsonify(user_object.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id=None):
    """ delete a resource of my list of cities """

    user_object = storage.get(User, user_id)
    if user_object is None:
        abort(404, "Not found")

    storage.delete(user_object)
    storage.save()

    return jsonify("{}"), 200


@app_views.route("/users", methods=["POST"])
def create_new_user():
    """ create new resource by my list of amenities """

    user_object_json = request.get_json()
    if user_object_json is None:
        abort(400, "Not a JSON")

    if 'email' not in user_object_json.keys():
        abort(400, "Missing email")

    if 'password' not in user_object_json.keys():
        abort(400, "Missing password")

    user_object = User(**user_object_json)
    user_object.save()

    return jsonify(user_object.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"])
def update_a_user(user_id=None):
    """ update a resource of my objects """

    user_object_json = request.get_json()
    if user_object_json is None:
        abort(400, "Not a JSON")

    user_object = storage.get(User, user_id)
    if user_object is None:
        abort(404, "Not found")

    user_object.update(user_object_json)

    return jsonify(user_object.to_dict()), 200
