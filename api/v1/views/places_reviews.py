#!/usr/bin/python3
""" Module for storing indeces for the route to reviews. """
from api.v1.views.__init__ import app_views
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from models import storage
from models.review import Review
from api.v1.app import app
from flask import request, jsonify, abort, make_response


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def return_list_all_reviews_by_city(place_id):
    """ Returns reviews by place id. """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    list_reviews = place.reviews
    list_of_json_reviews = []
    for review in list_reviews:
        list_of_json_reviews.append(review.to_dict())
    return(jsonify(list_of_json_reviews), 200)


@app_views.route("/reviews/<review_id>", methods=["GET"],
                 strict_slashes=False)
def return_review_by_id(review_id):
    """ Returns review by id. """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return(jsonify(review.to_dict()), 200)


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_review_obj(review_id):
    """ Deletes a review object by id. """
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return({}, 200)
    abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def route_place_post(place_id):
    """State POST Route 32c11d3d-99a1-4406-ab41-7b6ccb7dd760 user
     place 3ebfaf23-cede-4cf0-964d-8afc17b11d02
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    obj = request.get_json()
    if obj is None:
        return make_response("Not a JSON", 400)
    if 'user_id' not in obj:
        abort(400, 'Missing user_id')
    user = storage.get(User, obj['user_id'])
    if user is None:
        abort(404)
    if 'text' not in obj:
        abort(400, 'Missing text')
    obj['place_id'] = place_id
    review = Review(**obj)
    storage.new(review)
    storage.save()
    return make_response(jsonify(review.to_dict()), 201)


# @app_views.route("/places/<place_id>/reviews", methods=["POST"],
#                  strict_slashes=False)
# def create_review_obj(place_id):
#     """ Creates a new review linked to a place. """
#     if storage.get(Place, place_id) is None:
#         abort(404)
#     data = request.get_json()
#     if data is None:
#         return(make_response('Not a JSON', 400))
#     if 'user_id' not in data:
#         abort(400, 'Missing user_id')
#     if storage.get(User, data['user_id']) is None:
#         abort(404)
#     if 'text' not in data:
#         abort(400, 'Missing text')
#     data['place_id'] = place_id
#     review = Review(**data)
#     review.save()
#     return(make_response(jsonify(review.to_dict()), 201))


@app_views.route("/reviews/<review_id>", methods=["PUT"],
                 strict_slashes=False)
def update_review_obj(review_id):
    """ Updates a review by its id. """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return(make_response('Not a JSON', 400))
    ignored_keys = ["id", "user_id", "place_id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(review, key, value)
    storage.save()
    return(make_response(jsonify(review.to_dict()), 200))
