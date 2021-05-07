#!/usr/bin/python3
""" Module for storing indeces for the route to amenities. """
from api.v1.views.__init__ import app_views
from models.amenity import Amenity
from models.review import Review
from models.place import Place
from models.state import State
from models.city import City
from models.user import User
from models import storage
from api.v1.app import app
from flask import request, jsonify, abort


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def return_list_all_amenities():
    """ Returns list of amenities. """
    all_amenities = storage.all(Amenity)
    list_all_amenities = []
    for obj in all_amenities.values():
        list_all_amenities.append(obj.to_dict())
    return(jsonify(list_all_amenities))
