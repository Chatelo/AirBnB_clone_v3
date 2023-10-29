#!/usr/bin/python3

"""
This file contains all routes
that handle everything related to places and reviews
"""


# Importing
from flask import jsonify, request
from models.place import Place
from models.review import Review
from models import storage
from api.v1.views import app_views


# Define a route to get review of a specific place
@app_views.route(
    '/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """
    Get review of a place specified by its id
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


# Define a route to get specific review
@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """
    Get a specific review based on its ID
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    return jsonify(review.to_dict())


# Define a route to delete specific review
@app_views.route(
    '/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """
    Deletes a specific review based on its ID
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    storage.delete(review)
    storage.save()
    return jsonify({}), 200


# Define a route to review a specific place
@app_views.route(
    '/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """
    Review a specific place based on its ID
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if 'text' not in data:
        abort(400, 'Missing text')

    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)

    review = Review(**data)
    review.place_id = place.id
    review.save()

    return jsonify(review.to_dict()), 201


# Define a route to update a specific review
@app_views.route(
    '/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """
    Update a specific review based on its id
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')

    # Update the Review object with all key-value pairs from data
    # While ignoring keys: 'id', 'user_id', 'place_id',
    # 'created_at', and 'updated_at'
    for key, value in data.items():
        if key not in ['id', 'user_id', 'place_id',
                       'created_at', 'updated_at']:
            setattr(review, key, value)

    storage.save()

    return jsonify(review.to_dict()), 200
