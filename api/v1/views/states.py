#!/usr/bin/python3
""" Module for storing indeces for the route to states. """
from flask import request, jsonify, abort
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route("/states", methods=["GET"])
def return_list_all_states():
    """ Returns list of states. """
    all_states = storage.all(State)
    list_all_states = []
    for obj in all_states.values():
        list_all_states.append(obj.to_dict())
    return(jsonify(list_all_states))


@app_views.route("/states/<state_id>", methods=["GET"])
def return_state_obj(state_id):
    """ Returns a states object. """
    obj_state = storage.get(State, state_id)
    if bool(obj_state) is True:
        return jsonify(obj_state.to_dict())
    abort(404)


@app_views.route("/states/<state_id>", methods=["DELETE"])
def delete_state_obj(state_id):
    """ deletes a states object by id. """
    obj_state = storage.get(State, state_id)
    if obj_state:
        storage.delete(obj_state)
        storage.save()
        return({})
    abort(404)


@app_views.route("/states", methods=["POST"])
def create_state_obj():
    """ Creates a State object. """
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if 'name' not in data.keys():
        abort(400, "Missing name")
    else:
        state_obj = State(**data)
        state_obj.save()
        return(jsonify(state_obj.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=["PUT"])
def update_state_obj(state_id):
    """ Updates a State object. """
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    ignored_keys = ["id", "created_at", "updated_at"]
    state_obj = storage.get(State, state_id)
    if state_obj:
        for key, value in data.items():
            if key not in ignored_keys:
                setattr(state_obj, key, value)
                state_obj.save()
        return(jsonify(state_obj.to_dict()))
    abort(404)
