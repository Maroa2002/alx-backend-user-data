#!/usr/bin/env python3
""" Basic Authentication """
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ Basic Authentication class """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Returns Base64 part of Authorization header for Basic Authentication

        Args:
            authorization_header (str): The Authorization header.

        Returns:
            str: Base64 part of the Authorization header, or None if not valid
        """
        if authorization_header is None:
            return None

        if not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header[len("Basic "):]
