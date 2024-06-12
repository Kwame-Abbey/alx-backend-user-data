#!/usr/bin/env python3
"""Defines a hashed password
method using brcpyt package"""
import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


def _hash_password(password: str) -> bytes:
    """Takes in a string argument
    Args:
        password (str): Password of user
    Returns:
        Salted hash of the input password in bytes
    """
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed_password


def _generate_uuid() -> str:
    """Return a string representation of a new UUID"""
    random_id = str(uuid.uuid4())
    return random_id


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers new users
        Args:
            email (str): email of the user
            password (str): password of the new user
        Returns:
            The User object
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f'User {email} already exists')
        except NoResultFound:
            hashed_password = _hash_password(password).decode('utf-8')
            new_user = self._db.add_user(email, hashed_password)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """Credentials validation
        Args:
            email (str): email of user
            password (str): password of the user
        Returns:
            True of False
        """
        if not email or not password:
            return False
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode(),
                              user.hashed_password.encode('utf-8')):
                return True
            else:
                return False
        except (NoResultFound, InvalidRequestError):
            return False

    def create_session(self, email: str) -> str:
        """Get session ID
        Args:
            email (str): email of the user
        Returns:
            Seesion id
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except (NoResultFound, ValueError):
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """Find user by session ID
        Args:
            session_id (str): Session Id of user
        Returns:
            The corresponding User or None
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return User
        except (NoResultFound, ValueError):
            return None
