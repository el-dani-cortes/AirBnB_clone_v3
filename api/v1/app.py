#!/usr/bin/python3
""" Flask module, returs status of the api. """
from models import storage
from flask import Flask, jsonify, make_response
from os import getenv as env
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_connection(exception):
    """ Closes the session's connection. """
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """ Error handler 404, for Not found response."""
    return make_response({"error": "Not found"}, 404)

if __name__ == "__main__":
    host = "0.0.0.0"
    port = "5000"
    if env("HBNB_API_HOST"):
        host = env("HBNB_API_HOST")
    if env("HBNB_API_PORT"):
        port = env("HBNB_API_PORT")
    app.run(host=host, port=port, threaded=True)
