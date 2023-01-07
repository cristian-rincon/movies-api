"""This module contains routes related to users."""

import csv
from io import StringIO
from typing import Any

from fastapi import APIRouter, Depends, File
from sqlalchemy.orm import Session

from app.config import database, oauth2
from app.schemas import user as user_schema
from app.services import user as user_service

router = APIRouter(tags=["users"], prefix="/user")
get_db = database.get_db


@router.post("", response_model=user_schema.UserResponse)
def create_user(
    request: user_schema.User, db: Session = Depends(get_db)
) -> user_schema.UserResponse:
    """Create a new user.

    Args:
        request (user_schema.User): The user to create.
        db (Session, optional): The database session. If not provided, it
            will be obtained from the dependency injection system.

    Returns:
        user_schema.UserResponse: The created user.
    """
    return user_service.create(request, db)


@router.get("/{id}", response_model=user_schema.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)) -> Any:
    """Get a user by id.

    Args:
        id (int): The id of the user to get.
        db (Session, optional): The database session. If not provided, it
            will be obtained from the dependency injection system.

    Returns:
        user_schema.UserResponse: The user with the given id.
    """
    return user_service.get_one(id, db)


@router.post("/bulk")
def bulk_load_users(
    incoming_file: bytes = File(...),
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(oauth2.get_current_user),
) -> str:
    """Bulk load users from a CSV file.

    Args:
        incoming_file (bytes, optional): The CSV file to load.
        db (Session, optional): The database session. If not provided, it
            will be obtained from the dependency injection system.
        current_user (user_schema.User, optional): The current user. If
            not provided, it will be obtained from the dependency injection
            system.

    Returns:
        str: The number of users loaded.
    """
    _ = current_user
    content = incoming_file.decode()
    incoming_file = StringIO(content)  # type: ignore
    reader = csv.reader(incoming_file, delimiter=",")  # type: ignore
    header = next(reader)
    data: list = []
    if header is not None:
        data.extend(tuple(row) for row in reader)
    user_service.bulk_load(data, db)
    return f"{len(data)} users loaded"
