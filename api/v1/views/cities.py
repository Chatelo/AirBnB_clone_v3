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
import datetime


def UtcNow():
    """
    Get current time
    """
    now = datetime.datetime.utcnow()

    return now.strftime("%Y-%m-%dT%H:%M:%S.%f")


# Define a route to get all cities
@app_views.route('/cities', methods=['GET'], strict_slashes=False)
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
    '/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
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
    '/cities/<city_id>', methods=['GET'], strict_slashes=False)
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
    '/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
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
    '/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
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
                "error": "Not a JSON"
            }
        ), 400

    # Check if the required 'name' field is present in the JSON data
    if 'name' not in data:
        return jsonify(
            {
                "error": "Missing name"
            }
        ), 400

    # Create a new City object and set its attributes
    new_city = City(
        state_id=state.id,  # Set the state_id from the URL parameter
        name=data['name'],  # Set the city name from the JSON data
        created_at=UtcNow(),  # Set created_at using current UTC time
        updated_at=UtcNow()  # Set updated_at using current UTC time
    )

    # Add the new city to the state's cities
    state.cities.append(new_city)

    # Save the changes to the database
    storage.save()

    response = new_city.to_dict()
    response["__class__"] = "City"

    # Return the newly created city with a 201 status code
    return jsonify(response), 201


# Define a route to update details of a specified city
@app_views.route('/cities/<city_id>', methods=['PUT'])
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

    data = request.get_json()

    if data is None:
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
