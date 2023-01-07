"""Hashing configuration.
"""

from typing import Any
from passlib.context import CryptContext

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


def bcrypt(password: str) -> Any:
    """Hash password using bcrypt."""
    return pwd_ctx.hash(password)


def verify(plain_password: str, hashed_password: str) -> Any:
    """Verify password."""

    return pwd_ctx.verify(plain_password, hashed_password)
