"""This module contains functions related to authentication and authorization."""

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from app.schemas.token import TokenData
from app.routers.JWToken import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
    """Get the current user based on the provided token.

    Args:
        token (str, optional): The authentication token. If not provided,
            it will be obtained from the `Authorization` header.

    Returns:
        TokenData: The data contained in the token.
    """
    return verify_token(token)
