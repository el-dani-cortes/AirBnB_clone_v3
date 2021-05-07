#!/usr/bin/python3
""" Module for storing indeces for the route to states. """
from api.v1.views.__init__ import app_views
from models.state import State
from models.city import City
from models import storage
from api.v1.app import app
from flask import request, jsonify, abort


# Cities by state route. - - - - - - - - - - - - - - - - - - - - - - - - - - -|
@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def return_list_all_cities_by_state(state_id):
    """ Returns cities by state id. """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    list_cities = state.cities
    list_of_json_cities = []
    for city in list_cities:
        list_of_json_cities.append(city.to_dict())
    return(jsonify(list_of_json_cities))


# City by id route. - - - - - - - - - - - - - - - - - - - - - - - - - - - - - |
@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def return_city_by_id(city_id):
    """ Returns city by id. """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return(jsonify(city.to_dict()))


# City by id DELETE route. - - - - - - - - - - - - - - - - - - - - - - - - - -|
@app_views.route("/cities/<city_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_city_obj(city_id):
    """ Deletes a city object by id. """
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return({})
    abort(404)
