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


@app.route("/<string:lang>/<string:text>", strict_slashes=False)
def c_n_python(text, lang):
    """ the c is fun and Python is cool page"""
    if lang.lower() in ['python', 'c']:
        text = text.replace('_', ' ')
        lang = lang.capitalize()
        return f"{escape(lang)} {escape(text)}"
    abort(404)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
