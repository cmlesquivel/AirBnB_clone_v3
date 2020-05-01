#!/usr/bin/python3
""" list the routes allow in our app"""

from models import storage
from models.state import State

from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route("/states", methods=["GET"])
def get_states():
    """ display all the resources rest API """

    all_states = storage.all('State').values()
    all_stat = [istate.to_dict() for istate in all_states]

    return jsonify(all_stat)


@app_views.route("/states/<state_id>", methods=["GET"])
def get_states_by_name(state_id=None):
    """ display a resource of my list of states """

    state_object = storage.get(State, state_id)
    if state_object is None:
        abort(404, "Not found")

    return jsonify(state_object.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"])
def delete_state(state_id=None):
    """ delete a resource of my list of states """

    state_object = storage.get(State, state_id)
    if state_object is None:
        abort(404, "Not found")

    storage.delete(state_object)
    storage.save()

    return jsonify("{}"), 200


@app_views.route("/states", methods=["POST"])
def create_new_state():
    """ create new resource by my list of states """

    state_object_json = request.get_json()
    if state_object_json is None:
        abort(400, "Not found")

    if 'name' not in state_object_json.keys():
        abort(400, "Not found")

    object_state = State(**state_object_json)
    object_state.save()

    return jsonify(object_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"])
def update_a_state(state_id=None):
    """ update a resource of my objects """

    state_object_json = request.get_json()
    if state_object_json is None:
        abort(400, "Not found")

    state_object = storage.get(State, state_id)
    if state_object is None:
        abort(404, "Not found")

    state_object.update(state_object_json)

    return jsonify(state_object.to_dict()), 200
