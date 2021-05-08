#!/usr/bin/python3
""" Flask module, returs status of the api. """
from api.v1.views import app_views
from flask import Flask
from models import storage
from os import getenv as env

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_connection(exception):
    """ Closes the session's connection. """
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """ Error handler 404, for Not found response."""
    return {"error": "Not found"}, 404


if __name__ == "__main__":
    host = env("HBNB_API_HOST", "0.0.0.0")
    port = int(env("HBNB_API_PORT", "5000"))
    app.run(host=host, port=port, threaded=True)
