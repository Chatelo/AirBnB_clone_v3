#!/usr/bin/python3

"""
This file contains all routes
that handle everything related to cities
"""

# Importing
from flask import jsonify, request
from models.city import City
from models.state import State
from models import storage
from api.v1.views import app_views


# Define a route to get all cities
@app_views.route('/cities', method=['GET'], strict_slashes=False)
def get_all_cities():
    """
    Retrieve all cities from db
    """
    cities = storage.all(City).values()
    cities_list = []
    for city in cities:
        cities_list.append(city.to_dict())

    return jsonify(cities_list), 200


# Define a route to get all cities of a state
@app_views.route(
    '/states/<uuid:state_id>/cities', method=['GET'], strict_slashes=False)
def get_cities_of_state(state_id):
    """
    Retrieve all cities belonging to
    a given state based on state id
    """
    state = storage.get(State, state_id)
    if not state:
        return jsonify(
            {
                "error": "Not found"
            }
        ), 404

    cities_list = []
    for city in state.cities:
        cities_list.append(city.to_dict())
    return jsonify(cities_list), 200


# Define a route to get details of a city based on ID
@app_views.route(
    '/cities/<uuid:city_id>', method=['GET'], strict_slashes=False)
def get_details_of_a_city(city_id):
    """
    Retrieve all details of a city
    based on its ID
    """
    city = storage.get(City, city_id)
    if not city:
        return jsonify(
            {
                "error": "Not found"
            }
        ), 404

    return jsonify(city.to_dict()), 200


# Define a route to delete a city based on ID
@app_views.route(
    '/cities/<uuid:city_id>', method=['DELETE'], strict_slashes=False)
def delete_a_city(city_id):
    """
    Delete a city based on provided ID
    if it exists
    """
    city = storage.get(City, city_id)
    if not city:
        return jsonify(
            {
                "error": "Not found"
            }
        ), 404

    # If the City object exists, delete it
    storage.delete(city)

    # Return an empty dictionary with a 200 status code
    return jsonify({}), 200


# Define a route to create a city
@app_views.route(
    '/states/<state_id>/cities', method=['POST'], strict_slashes=False)
def create_a_city(state_id):
    """
    Create a city in a state provided
    by its ID
    """
    state = storage.get(State, state_id)
    if not state:
        return jsonify(
            {
                "error": "Not found"
            }
        ), 404

    data = request.get_json()

    if data is None:
        return jsonify(
            {
                "error": "Invalid JSON"
            }
        ), 400

    # Check if the required 'name' field is present in the JSON data
    if 'name' not in data:
        return jsonify(
            {
                "error": "Missing 'name' field in JSON data"
            }
        ), 400

    # Create a new City object and set its attributes
    new_city = City(
        state_id=state.id,  # Set the state_id from the URL parameter
        name=data['name']  # Set the city name from the JSON data
    )

    # Add the new city to the state's cities
    state.cities.append(new_city)

    # Save the changes to the database
    storage.save()

    # Return the newly created city with a 201 status code
    return jsonify(new_city.to_dict()), 201


# Define a route to update details of a specified city
@app_views.route('/api/v1/cities/<uuid:city_id>', methods=['PUT'])
def update_a_city(city_id):
    """
    Update details of a city based on its ID
    """
    # Retrieve the City object based on the city_id
    city = storage.get(City, city_id)

    if not city:
        return jsonify(
            {
                "error": "City not found"
            }
        ), 404

    try:
        # Attempt to get JSON data from the request's body
        data = request.get_json()
    except ValueError:
        # If JSON parsing fails, return a 400 error response
        return jsonify(
            {
                "error": "Not a JSON"
            }
        ), 400

    # Define keys to ignore when updating the City object
    ignored_keys = ['id', 'state_id', 'created_at', 'updated_at']

    # Update the City object with key-value pairs from the JSON data
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(city, key, value)

    # Save the changes to the database
    storage.save()

    # Return the updated City object with a 200 status code
    return jsonify(city.to_dict()), 200