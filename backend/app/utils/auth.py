from datetime import datetime, timezone, timedelta

import jwt

from app.config import settings
from app.models.user import User
from app.services.exceptions import Unauthorized
from app.utils import generate_uid


def create_jwt(payload: dict, expires_delta: timedelta) -> str:
    """
    Create a JWT token with the payload and expiration time.
    :param payload: The payload to include in the token.
    :param expires_delta: The expiration time for the token.
    :return: The JWT token.
    """
    iat = datetime.now(timezone.utc)
    exp = iat + expires_delta
    jti = generate_uid(23)

    claims = {"iat": iat, "jti": jti, "nbf": iat, "exp": exp, **payload}

    token = jwt.encode(payload=claims, key=settings.SECRET_KEY, algorithm="HS256")
    return token


def create_access_token(user: User, fresh: bool):
    """
    Create an access token for the user.
    :param user: The user to create the token for.
    :param fresh: If the access token is fresh
    :return: The access token.
    """
    role = user.role
    permissions = user.scopes
    payload = {
        "type": "access",
        "fresh": fresh,
        "sub": user.uid,
        "role": role.name,
        "scopes": permissions,
    }
    return create_jwt(
        payload, expires_delta=timedelta(seconds=settings.access_token_expires)
    )


def create_refresh_token(user: User):
    """
    Create a refresh token for the user.
    :param user: The user to create the token for.
    :return: The refresh token.
    """
    payload = {"type": "refresh", "sub": user.uid}
    return create_jwt(
        payload, expires_delta=timedelta(seconds=settings.refresh_token_expires)
    )


def verify_jwt(token: str):
    """
    Verify a JWT token.
    :param token: The token to verify.
    :return: The claims from the token.
    """
    try:
        claims = jwt.decode(token, key=settings.SECRET_KEY, algorithms=["HS256"])
        return claims
    except jwt.PyJWTError as e:
        print("Error verifying token:", e)
        raise Unauthorized("Invalid token")
