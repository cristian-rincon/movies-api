"""This module contains models related to users."""

from sqlalchemy import Column, Integer, String

from app.config.database import Base


class User(Base):
    """Model representing a user.

    Attributes:
        id (int): The user's id.
        name (str): The user's name.
        email (str): The user's email address.
        password (str): The user's password.
    """

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
