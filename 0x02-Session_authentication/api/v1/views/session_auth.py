#!/usr/bin/env python3
"""A new Flask view that handles all
routes for the Session authentication
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
import os


@app_views.route(
    '/auth_session/login', methods=['POST'], strict_slashes=False)
def session_authentication():
    """ handles all routes for
    the Session authentication
    """
    email = request.form.get('email')
    if not email:
        return jsonify({"error": "email missing"}), 400

    password = request.form.get('password')
    if not password:
        return jsonify({"error": "password missing"}), 400

    try:
        users = User.search({"email": email})
    except Exception:
        return None

    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    for user in users:
        if not user.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    user = users[0]
    session_id = auth.create_session(user.id)

    session_name = os.getenv("SESSION_NAME")

    response = jsonify(user.to_json())
    response.set_cookie(session_name, session_id)

    return response
