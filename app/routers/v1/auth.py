"""This module contains routes related to authentication."""

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.config import database, hashing
from app.config.settings import ACCESS_TOKEN_EXPIRE_MINUTES
from app.routers.JWToken import create_access_token
from app.models.user import User as UserORM

router = APIRouter(
    prefix="",
    tags=["authentication"],
)

get_db = database.get_db


@router.post("/login")
def login(
    request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
) -> dict:
    """Log in a user.

    Args:
        request (OAuth2PasswordRequestForm, optional): The login request.
            If not provided, it will be obtained from the dependency injection
            system.
        db (Session, optional): The database session. If not provided, it
            will be obtained from the dependency injection system.

    Returns:
        Token: An access token for the user.

    Raises:
        HTTPException: If the user's credentials are invalid.
    """

    user = db.query(UserORM).filter(UserORM.email == request.username).first()

    if user is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials."
        )

    if not hashing.verify(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials."
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
