#!/usr/bin/env python3
"""4. Hash password"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    returned bytes is a salted hash of the input
    password, hashed with bcrypt.hashpw
    """
    if password is None:
        raise ValueError("Password must not be None")

    salt = bcrypt.gensalt()
    password_in_bytes = password.encode('utf-8')
    hash_password = bcrypt.hashpw(
        password=password_in_bytes,
        salt=salt
    )
    return hash_password
