#!/usr/bin/env python3
"""Module for API authentication"""
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """template for all authentication system"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ require auth """
        if path is None:
            return True

        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        normalized_path = path if path.endswith("/") else path + "/"

        if normalized_path in excluded_paths:
            return False

        return True

    def authorization_header(self, request=None) -> str:
        """ Authorization header """
        if request is None:
            return None

        # Get the authorization header from the request
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return None

        return auth_header

    def current_user(self, request=None) -> TypeVar('User'):
        """ current user """
        return None

    def session_cookie(self, request=None):
        """Returns a cookie from a request"""
        if request is None:
            return None
        _my_session_id = getenv("SESSION_NAME")
        return request.cookies.get(_my_session_id)
