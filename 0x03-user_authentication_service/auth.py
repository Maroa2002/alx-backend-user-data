#!/usr/bin/env python3
"""Auth module"""
import bcrypt
from db import DB
from user import User


def _hash_password(password: str):
    """Hashes Password"""
    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_pwd


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Implements user registration"""
        user = self._db.find_user_by(email=email)
        if user:
            raise ValueError(f"User {email} already exists")
        else:
            hashed_pwd = _hash_password(password)

        new_user = self._db.add_user(email, hashed_pwd)

        return new_user
