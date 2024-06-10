#!/usr/bin/env python3
"""Defines a Basic Flask App"""
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def home():
    """Returns a json message"""
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
