"""This module provides functionality to work with JWT."""

import datetime
import jwt

DEFAULT_EXP_TIME = 86400


def encode_jwt(data, secret_key, exp_time=DEFAULT_EXP_TIME):
    """Create JWT for data payload with secret key and certain expiration time."""
    if exp_time is not None:
        data["exp"] = datetime.datetime.now() + datetime.timedelta(seconds=exp_time)

    token = jwt.encode(data, secret_key)
    return token


def decode_jwt(token, secret_key):
    """Try to decode JWT with secret key."""
    try:
        token = jwt.decode(token, secret_key)
    except (jwt.ExpiredSignatureError, jwt.DecodeError):
        return None

    return token
