#!/usr/bin/env python3
"""6. Basic auth"""
import base64
import binascii
from typing import TypeVar
from models.user import User

from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Defines the basic auth class"""

    def extract_base64_authorization_header(
            self,
            authorization_header: str
    ) -> str:
        """returns the Base64 part of the Authorization
        header for a Basic Authentication
        """
        if authorization_header is None:
            return None

        if type(authorization_header) is not str:
            return None

        if authorization_header.startswith('Basic ') is False:
            return None

        return authorization_header.split(' ')[1]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str
    ) -> str:
        """returns the decoded value of a
         Base64 string base64_authorization_header
        """
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None

        try:
            data = base64.b64decode(base64_authorization_header)
            return data.decode('utf-8')
        except (binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str
    ) -> (str, str):
        """
        returns the user email and password from the Base64 decoded value
        """

        if not decoded_base64_authorization_header:
            return None, None

        if type(decoded_base64_authorization_header) is not str:
            return None, None

        if ":" not in decoded_base64_authorization_header:
            return None, None

        user_info = decoded_base64_authorization_header.split(':')
        return user_info[0], user_info[1]

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """
        returns the User instance based on his email and password.
        """

        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        user_list = User.search({"email": user_email})
        if not user_list:
            return None
        user = user_list[0]
        if not user.is_valid_password(user_pwd):
            return None

        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves all the objects using all the functions"""
        auth_header = super().authorization_header(request)

        if auth_header:
            bas64_headr = self.extract_base64_authorization_header(auth_header)

            if bas64_headr:
                decoded_base64 = self.decode_base64_authorization_header(
                    bas64_headr)

                if decoded_base64:
                    email, password = self.extract_user_credentials(
                        decoded_base64)
                    user = self.user_object_from_credentials(email, password)
                    return user
        return None
