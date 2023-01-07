"""Movie Pydantic model for API."""

from typing import Union

from pydantic import BaseModel, Field


class Movie(BaseModel):
    """Movie Pydantic model.

    Attributes:
        title (str): Movie title.
        overview (str): Movie overview.
        year (int): Movie year.
        rating (int): Movie rating.
        genre (str): Movie genre.

    """

    title: str = Field(..., max_length=100)
    overview: str = Field(..., max_length=500)
    year: int = Field(..., gt=1900, lt=2022)
    rating: Union[int, float] = Field(..., gt=0.0, lt=10.0)
    genre: str = Field(..., max_length=100)

    class Config:
        """Pydantic config."""

        schema_extra = {
            "example": {
                "title": "The Shawshank Redemption",
                "overview": "Two imprisoned",
                "year": 1994,
                "rating": 9.3,
                "genre": "Drama",
            }
        }


class BaseUser(BaseModel):
    """Base user Pydantic model."""

    username: str = Field(..., max_length=50)
    password: str = Field(..., max_length=50)
