#!/usr/bin/python3

"""
Check status of API
"""

from flask import jsonify
from api.v1.views import app_views
from models import *


@app_views.route('/status', strict_slashes=False)
def check_status():
    """
    Check status of API
    """
    return jsonify(
        {
            "status": "OK"
        }
    ), 200


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def check_stats():
    """
    Check stats of all objects.
    """
    try:
        storage.reload()
        stats = {
            "amenities": storage.count("Amenity"),
            "cities": storage.count("City"),
            "places": storage.count("Place"),
            "reviews": storage.count("Review"),
            "states": storage.count("State"),
            "users": storage.count("User")
        }
        return jsonify(stats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
