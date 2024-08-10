#!/usr/bin/env python3
"""7. New view for Session Authentication"""
from api.v1.views import app_views
from flask import request, jsonify
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login():
    """handles all routes for the Session authentication"""
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or email == "":
        return jsonify({"error": "email missing"}), 400
    if not password or password == "":
        return jsonify({"error": "password missing"}), 400

    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    for user in users:
        found_user_bool = user.is_valid_password(password)
        if user.is_valid_password(password):
            found_user = user
    if not found_user_bool:
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(found_user.id)
    session_name = getenv("SESSION_NAME")

    response = jsonify(found_user.to_json())
    response.set_cookie(session_name, session_id)
    return response


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def destroy_session(self, request=None):
    """ Logout user by destroying session """
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
