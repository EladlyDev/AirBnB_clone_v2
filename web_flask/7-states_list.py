#!/usr/bin/python3
"""
    7-states_list module
    1 route renders a template with dynamic content
"""
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


@app.route("/states_list", strict_slashes=False)
def states_list():
    """
        the states_list route that
        renders all states from storage
    """
    states = storage.all(State).values()
    return render_template('7-states_list.html', states=states)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
