#!/usr/in/python3
""" This script will start a FLASK WEB APPLICATION """
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from os import environ
from flask import Flask, render_template
import uuid

app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(error):
    """ shuts down the storage """
    storage.close()


@app.route('/2-hbnb', strict_slashes=False)
def hbnb():
    """ function to sort states, amenities and places """
    states = storage.all(State).values()
    states = sorted(states, key=lambda k: k.name)
    states_city = []

    for state in states:
        states_city.append([state, sorted(state.cities, key=lambda k: k.name)])

    amenities = storage.all(Amenity).values()
    amenities = sorted(amenities, key=lambda k: k.name)

    places = storage.all(Place).values()
    places = sorted(places, key=lambda k: k.name)
    cache_id = uuid.uuid4()
    return render_template(
            '2-hbnb.html',
            states=states_city,
            amenities=amenities,
            places=places,
            cache_id=cache_id)


if __name__ == "__main__":
    """ setting the host and port """
    app.run(host='0.0.0.0', port=5000)
