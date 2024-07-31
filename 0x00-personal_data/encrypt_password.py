#!/usr/bin/env python3
""" Encrypting passwords """
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt with a salt.

    Args:
        password (str): The plain text password to hash.

    Returns:
        bytes: The salted, hashed password as a byte string.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password
