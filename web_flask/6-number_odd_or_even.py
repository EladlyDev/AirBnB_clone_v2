#!/usr/bin/python3
""" a script that starts a Flask web application """
from flask import Flask, abort, render_template
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


@app.route('/<string:lang>/<string:text>', strict_slashes=False)
def c_n_python(text, lang):
    """ the c is fun and Python is cool page"""
    if lang.lower() in ['python', 'c']:
        text = text.replace('_', ' ')
        lang = lang.capitalize()
        return f"{escape(lang)} {escape(text)}"
    abort(404)


@app.route('/number/<int:n>', strict_slashes=False)
def number_route(n):
    """ Works only if n is a valid number """
    return f"{n} is a number"


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template_route(n):
    """ Works only if n is a valid number """
    return render_template('5-number.html', n=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_odd_or_even_route(n):
    """ Works only if n is a valid number """
    return render_template('6-number_odd_or_even.html', n=n)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
