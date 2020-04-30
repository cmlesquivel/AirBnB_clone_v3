#!/usr/bin/python3
# list the routes allow in our app
from models import storage
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from api.v1.views import app_views
from flask import jsonify

classes = {"amenities": Amenity, "cities": City, "places": Place,
           "reviews": Review, "states": State, "users": User}


@app_views.route("/status")
def show_status():
    """ Show the status """
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def show_stats():
    """ Show the quantity of objects classified by class """

    totales = {}
    for key, value in classes.items():
        totales[key] = storage.count(value)

    return jsonify(totales)
