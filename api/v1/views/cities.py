#!/usr/bin/python3
""" Module for storing indeces for the route to states. """
from api.v1.views.__init__ import app_views
from models.state import State
from models.city import City
from models import storage
from api.v1.app import app
from flask import request, jsonify, abort



@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def return_list_all_cities_by_state(state_id):
    """ Returns list of states. """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    list_cities = state.cities
    list_of_json_cities = []
    for city in list_cities:
        list_of_json_cities.append(city.to_dict())
    return(jsonify(list_of_json_cities))
