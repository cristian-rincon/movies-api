"""This module contains models related to tokens."""

from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    """Model representing an access token.

    Attributes:
        access_token (str): The token string.
        token_type (str): The type of token.
    """

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Model representing data contained in an access token.

    Attributes:
        email (Optional[str], optional): The user's email address.
    """

    email: Optional[str] = None
