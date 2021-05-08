#!/usr/bin/python3
""" Flask module, returns status of the api. """
from api.v1.views import app_views
from os import getenv as env
from models import storage
from flask import Flask
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
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
    app.run(host=host, port=port, threaded=True, debug=True)
