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

        for ex_path in excluded_paths:
            if ex_path.endswith('*'):
                if path.startswith(ex_path[:-1]):
                    return False
            else:
                if not path.endswith('/'):
                    path += '/'
                if path == ex_path:
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """Retrieves the authorization header from the request."""
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves the current user from the request."""
        return None
