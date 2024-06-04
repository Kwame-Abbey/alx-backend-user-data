#!/usr/bin/env python3
"""Defines an auth class"""
from flask import request
from typing import List, TypeVar
from models.user import User


class Auth:
    """Template for all authentication system"""

    def __init__(self) -> None:
        pass

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Returns a boolean"""
        return False

    def authorization_header(self, request=None) -> str:
        """Returns None"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns None"""
        return None
