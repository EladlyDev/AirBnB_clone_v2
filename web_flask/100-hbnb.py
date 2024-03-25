#!/usr/bin/python3
""" starts a Flask web application the contains the route /cities_by_states """
from flask import Flask, render_template
from models.state import State
from models.amenity import Amenity
from models.place import Place
from models.user import User
from models import storage

app = Flask(__name__)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """ colses the connectetion """
    storage.close()


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """ shows the hbnb website, from db to the view! """
    states = storage.all(State).values()
    amenities = storage.all(Amenity).values()
    places = storage.all(Place).values()
    users = storage.all(User).values()
    return render_template('100-hbnb.html', states=states,
                           amenities=amenities, places=places,
                           users=users)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
