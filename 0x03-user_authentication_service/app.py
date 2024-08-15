#!/usr/bin/env python3
"""Creates a simple flask app"""
import flask
from flask import Flask, request, abort, make_response, redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def home():
    """Home page"""
    return flask.jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'], strict_slashes=False)
def users():
    """Checks if the user with the given email is created already or not"""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email, password)
        return flask.jsonify({"email": email, "message": "user created"})
    except ValueError as err:
        return flask.jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=['POST'], strict_slashes=False)
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


@app.route("/sessions", methods=['DELETE'], strict_slashes=False)
def logout():
    """Deletes the session with the current cookie"""
    session_id = request.cookies.get('session_id')
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            AUTH.destroy_session(user.id)
            return redirect("/")
    abort(403)


@app.route("/profile", methods=['GET'], strict_slashes=False)
def profile():
    """Checks if the user  with the cookie exist"""
    session_id = request.cookies.get('session_id')

    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            return flask.jsonify({"email": user.email}), 200
    abort(403)


@app.route("/reset_password", methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """Resets password of the given email"""
    email = request.form.get('email')
    try:
        token = AUTH.get_reset_password_token(email)
        return flask.jsonify({"email": email, "reset_token": token}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
