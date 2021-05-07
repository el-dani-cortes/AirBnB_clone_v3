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


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def return_amenity_obj(amenity_id):
    """ Returns an Amenity object. """
    obj_amenity = storage.get(Amenity, amenity_id)
    if obj_amenity:
        return jsonify(obj_amenity.to_dict())
    abort(404)


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity_obj(amenity_id):
    """ deletes a amenity object by id. """
    obj_amenity = storage.get(Amenity, amenity_id)
    if obj_amenity:
        key = 'Amenity.' + obj_amenity.id
        storage.delete(obj_amenity)
        storage.save()
        return({})
    abort(404)


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity_obj():
    """ Creates a Amenity object. """
    try:
        data = request.get_json()
    except:
        abort(400, 'Not a JSON')
    if 'name' not in data.keys():
        abort(400, "Missing name")
    else:
        amenity_obj = Amenity(**data)
        amenity_obj.save()
        return(jsonify(amenity_obj.to_dict()), 201)
