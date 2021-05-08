#!/usr/bin/python3
""" Module for storing endpoints for the users routes. """
from flask import request, jsonify, abort
from api.v1.views import app_views
from models.user import User
from models import storage


# All users route. - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -|
@app_views.route("/users", methods=["GET"])
def return_all_users():
    """ Returns all users. """
    users = storage.all(User)
    if users is None:
        abort(404)
    list_of_json_users = []
    for user in users:
        list_of_json_users.append(city.to_dict())
    return(jsonify(list_of_json_users))


# User by id route. - - - - - - - - - - - - - - - - - - - - - - - - - - - - - |
@app_views.route("/user/<user_id>", methods=["GET"])
def return_user_by_id(user_id):
    """ Returns user by id. """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return(user.to_dict())


# User by id DELETE route. - - - - - - - - - - - - - - - - - - - - - - - - - -|
@app_views.route("users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    """ Deletes a user object by id. """
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return({})
    abort(404)


# Create user. - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -|
@app_views.route("/api/v1/users", methods=["POST"])
def create_city_obj():
    """ Creates a new City linked to a State.  """
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if 'email' not in data.keys():
        abort(400, "Missing email")
    if 'password' not in data.keys():
        abort(400, "Missing password")
    if storage.get(User, ) is None:
        abort(404)
    city = City(**data)
    city.save()
    return(city.to_dict(), 201)


# Update a city by its id. - - - - - - - - - - - - - - - - - - - - - - - - - -|
@app_views.route("/api/v1/users/<user_id>", methods=["PUT"])
def update_city_obj(user_id):
    """ Updates a city by its id. """
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    ignored_keys = ["id", "email", "created_at", "updated_at"]
    user = storage.get(User, user_id)
    if user:
        for key, value in data.items():
            if key not in ignored_keys:
                setattr(user, key, value)
                user.save()
        return(user.to_dict())
    abort(404)
