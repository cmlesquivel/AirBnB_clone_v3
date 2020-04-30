#!/usr/bin/python3
# create our module Flask
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv


host = getenv("HBNB_API_HOST", "0.0.0.0")
port = getenv("HBNB_API_PORT", 5000)

app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def normal404(e):
    """ creation web error 404 """
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def shotdown_session(exception=None):
    """ remove the current SQLAlchemy Session: """
    storage.close()

if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)
