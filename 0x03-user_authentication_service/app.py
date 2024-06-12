#!/usr/bin/env python3
"""Defines a Basic Flask App"""
from flask import Flask, jsonify, request, abort, redirect, url_for
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def home():
    """Returns a json message"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user():
    """Registers a new user"""
    user_email = request.form.get('email')
    user_password = request.form.get('password')
    try:
        AUTH.register_user(email=user_email, password=user_password)
        return jsonify({"email": user_email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """create a new session for the user,
    store it the session ID as a cookie with key "session_id"
    on the response and return a JSON payload of the form
    """
    user_email = request.form.get('email')
    user_password = request.form.get('password')

    if not AUTH.valid_login(user_email, user_password):
        abort(401)

    session_id = AUTH.create_session(user_email)
    response = jsonify({"email": user_email, "message": "logged in"})
    response.set_cookie('session_id', session_id)
    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """Find the user with the requested session ID.
    If the user exists destroy the session
    and redirect the user to GET /
    """
    session_id = request.cookies.get('session_id')
    if not session_id:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user_id=user.id)
    return redirect(url_for('home'))


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """
    Get user profile
    """
    session_id = request.cookies.get('session_id')
    if not session_id:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """Get reset password token"""
    email = request.form.get('email')
    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
