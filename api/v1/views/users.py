#!/usr/bin/python3

"""
This file contains all routes
that handle everything related to users
"""

# Importing
from flask import jsonify, request, abort
from models.user import User
from models import storage
from api.v1.views import app_views


# Define a route to get all users
@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """
    Retrieve all cities from db
    """
    users = storage.all(User).values()
    users_list = []
    for user in users:
        users_list.append(user.to_dict())

    return jsonify(users_list), 200


# Define a route to get user based on id
@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """
    Get a specific user by user_id.
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    return jsonify(user.to_dict()), 200


# Define a route to delete user based on ID
@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """
    Delete a user based on specific Id
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    storage.delete(user)
    storage.save()
    return jsonify({}), 200


# Define a route to create a new user
@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """
    Create a new user based on input
    """
    user_data = request.get_json()

    if user_data is None:
        abort(400, 'Not a JSON')

    if 'email' not in user_data:
        abort(400, 'Missing email')

    if 'password' not in user_data:
        abort(400, 'Missing password')

    user = User(**user_data)
    storage.new(user)
    storage.save()

    return jsonify(user.to_dict()), 201


# Define a route to update user details
@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """
    Update details of a specified user based on ID
    """
    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    user_data = request.get_json()

    if user_data is None:
        abort(400, 'Not a JSON')

    # Update the User object with all key-value pairs from user_data
    # While ignoring keys: 'id', 'email', 'created_at', and 'updated_at'
    for key, value in user_data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)

    storage.save()

    return jsonify(user.to_dict()), 200
