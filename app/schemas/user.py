"""User Pydantic models."""

from pydantic import BaseModel


class User(BaseModel):
    """Model representing a user.

    Attributes:
        name (str): The user's name.
        email (str): The user's email address.
        password (str): The user's password.
    """

    name: str
    email: str
    password: str


class UserResponse(BaseModel):
    """Model representing a response containing a user's name and email.

    Attributes:
        name (str): The user's name.
        email (str): The user's email address.
    """

    name: str
    email: str

    class Config:
        """Pydantic config class."""

        orm_mode = True
