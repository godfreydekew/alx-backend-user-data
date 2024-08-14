#!/usr/bin/env python3
"""4. Hash password"""
import uuid
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


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


def _generate_uuid() -> str:
    """
    Generates and returns a string representation of a new UUID.
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initialize db class"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Adds a new user to the database"""
        session = self._db._session
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f"User {email} already exists")

        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(
                email=email,
                hashed_password=hashed_password.decode('utf-8')
            )
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """Checks if the password is valid for the specific email"""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                encoded_p = password.encode('utf-8')
                user_password = user.hashed_password.encode('utf-8')
                return bcrypt.checkpw(encoded_p, user_password)
            else:
                return False
        except Exception:
            return False
