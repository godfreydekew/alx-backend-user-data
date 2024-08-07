#!/usr/bin/env python3
"""6. Basic auth"""
import base64
import binascii

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
        except binascii.Error as e:
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
