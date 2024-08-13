#!/usr/bin/env python3
"""Creates a simple flask app"""
import flask
from flask import Flask, request
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route("/")
def home():
    """Home page"""
    return flask.jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'])
def users():
    """Post request for users"""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email, password)
        return flask.jsonify({"email": email, "message": password})

    except Exception:
        return flask.jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
