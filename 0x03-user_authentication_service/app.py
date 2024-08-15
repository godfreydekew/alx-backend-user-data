#!/usr/bin/env python3
"""Creates a simple flask app"""
import flask
from flask import Flask, request, abort, make_response
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def home():
    """Home page"""
    return flask.jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'])
def users():
    """Checks if the user with the given email is created already or not"""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email, password)
        return flask.jsonify({"email": email, "message": "user created"})
    except ValueError as err:
        return flask.jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=['POST'])
def login():
    """Adds the session id as the cookie"""
    email = request.form.get('email')
    password = request.form.get('password')

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        if session_id:
            response = make_response({"email": email, "message": "logged in"})
            response.set_cookie("session_id", session_id)
            return response
    abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
