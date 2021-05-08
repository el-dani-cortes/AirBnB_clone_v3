#!/usr/bin/python3
""" Module for storing indeces for the route to places. """
from flask import request, jsonify, abort
from api.v1.views import app_views
from models.place import Place
from models.state import State
from models.city import City
from models.user import User
from models import storage


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def return_list_all_places_by_city(city_id):
    """ Returns places by city id. """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    list_places = city.places
    list_of_json_places = []
    for place in list_places:
        list_of_json_places.append(place.to_dict())
    return(jsonify(list_of_json_places))


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def return_place_by_id(place_id):
    """ Returns place by id. """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return(jsonify(place.to_dict()))


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_place_obj(place_id):
    """ Deletes a place object by id. """
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return({})
    abort(404)


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def create_place_obj(city_id):
    """ Creates a new place linked to a City. """
    try:
        data = request.get_json()
    except:
        abort(400, 'Not a JSON')
    if 'name' not in data.keys():
        abort(400, 'Missing name')
    if 'user_id' not in data.keys():
        abort(400, 'Missing user_id')
    if storage.get(City, city_id) is None:
        abort(404)
    if storage.get(User, data['user_id']) is None:
        abort(404)
    data['city_id'] = city_id
    place = Place(**data)
    place.save()
    return(jsonify(place.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=["PUT"],
                 strict_slashes=False)
def update_place_obj(place_id):
    """ Updates a place by its id. """
    try:
        data = request.get_json()
    except:
        abort(400, 'Not a JSON')
    ignored_keys = ["id", "user_id", "city_id", "created_at", "updated_at"]
    place = storage.get(Place, place_id)
    if place:
        for key, value in data.items():
            if key not in ignored_keys:
                setattr(place, key, value)
                place.save()
        return(jsonify(place.to_dict()))
    abort(404)
