"""Authentication module"""

from typing import Any
from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer
from jwt import decode, encode


def generate_token(data: dict) -> Any:
    """Generates a JWT token"""
    return encode(payload=data, key="secret", algorithm="HS256")


def verify_token(token: str) -> Any:
    """Verifies a JWT token"""
    return decode(jwt=token, key="secret", algorithms=["HS256"])


class JWTBearer(HTTPBearer):
    """JWT Bearer class"""

    async def __call__(self, request: Request) -> None:
        auth = await super().__call__(request)
        data = verify_token(auth.credentials)
        if data["username"] != "admin":
            raise HTTPException(status_code=401, detail="Invalid username")
