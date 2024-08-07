#!/usr/bin/env python3
"""3. Auth class"""
from flask import request
from typing import List, TypeVar


class Auth:
    """a class to manage the API authentication."""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Determines if authentication is required for a given path."""

        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        if not path.endswith('/'):
            path += '/'

        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """Retrieves the authorization header from the request."""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves the current user from the request."""
        return None
