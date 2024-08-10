#!/usr/bin/env python3
"""1. Empty session"""
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """A class to manage session authentication"""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ creates a Session ID for a user_id"""
        if not user_id:
            return None
        if not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id
        return session_id