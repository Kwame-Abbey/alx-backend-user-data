#!/usr/bin/env python3
"""Defines a hashed password
method using brcpyt package"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Takes in a string argument
    Args:
        password (str): Password of user
    Return:
        Salted hash of the input password in bytes
    """
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed_password
