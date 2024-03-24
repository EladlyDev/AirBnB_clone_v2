#!/usr/bin/python3
""" starts a Flask web application the contains the route /cities_by_states """
from flask import Flask, render_template
from models.state import State
from models import storage

app = Flask(__name__)


@app.teardown_request
def teardown_request(exception):
    """ called after each request """
    storage.close()


@app.teardown_appcontext
def teardown_appcontext(exception):
    """ colses the connectetion """
    storage.close()


@app.route("/states", strict_slashes=False)
def states():
    """ shows all states in the db"""
    states = [state for k, state in storage.all(State).items()]
    return render_template('9-states.html', states=states, route='states')


@app.route("/states/<string:id>", strict_slashes=False)
def states_id(id):
    """ shows the specific state """
    states = storage.all(State)
    id = "State.{}".format(id)
    return render_template('9-states.html', states=states,
                           route='states_id', id=id)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
