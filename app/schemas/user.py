"""User Pydantic models."""

from pydantic import BaseModel, Field


class BaseUser(BaseModel):
    """Base user Pydantic model."""

    username: str = Field(..., max_length=50)
    password: str = Field(..., max_length=50)
