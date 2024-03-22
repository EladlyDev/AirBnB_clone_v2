#!/usr/bin/python3
""" a script that starts a Flask web application """
from flask import Flask, abort
from markupsafe import escape

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def route():
    """ the root of the site """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """ returns the HBNB page """
    return "HBNB"


@app.route("/c/<string:text>", strict_slashes=False)
def c_is_fun(text):
    """ the c is fun page """
    text = text.replace('_', ' ')
    return f"C {escape(text)}"


@app.route("/python", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python(text="is cool"):
    """python route"""
    text = text.replace("_", " ")
    return f"Python {escape(text)}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
