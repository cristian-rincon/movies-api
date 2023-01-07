"""JWT Token"""


from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from fastapi import HTTPException, status
from jose import JWTError, jwt

from app.schemas.token import TokenData
from app.config.settings import ALGORITHM, SECRET_KEY


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> Any:
    """Create access token.

    Args:
        data (dict): Data to encode.
        expires_delta (Optional[timedelta], optional): Expiration time. Defaults to None.

    Returns:
        str: Encoded token.
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode["exp"] = expire
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> TokenData:
    """Verify the authenticity of the given token.

    Args:
        token (str): The token to verify.

    Returns:
        TokenData: The data contained in the token.

    Raises:
        HTTPException: If the token is invalid or could not be verified.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception

        return TokenData(email=email)
    except JWTError as e:
        raise credentials_exception from e
