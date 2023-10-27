#!/usr/bin/python3

"""
Start a simple flask REST API
for version 1 of our clone
"""

# Importing libraries and modules
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
import os


# Creating an instance of Flask
app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def close_db(exception):
    """
    Closes the storage on teardown
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ 404 Error
    ---
    responses:
      404:
        description: a resource was not found
    """
    return make_response(jsonify({'error': "Not found"}), 404)


if __name__ == "__main__":
    host = os.environ.get("HBNB_API_HOST", "0.0.0.0")
    port = int(os.environ.get("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
