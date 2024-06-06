#!/usr/bin/env python3
"""Creates a new authentication system,
based on Session ID stored in database
"""
from models.base import Base


class UserSession(Base):
    """Creates new authentication system"""

    def __init__(self, *args: list, **kwargs: dict):
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
