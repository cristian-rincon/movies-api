from typing import Union
from pydantic import BaseModel, Field

class Movie(BaseModel):
    id: int = Field(...)
    title: str = Field(..., max_length=100)
    overview: str = Field(..., max_length=500)
    year: int = Field(..., gt=1900, lt=2022)
    rating: Union[int, float] = Field(..., gt=0.0, lt=10.0)
    genre: str = Field(..., max_length=100)

    class Config:
        schema_extra = {
            "example": {
                "id": 9999,
                "title": "The Shawshank Redemption",
                "overview": "Two imprisoned",
                "year": 1994,
                "rating": 9.3,
                "genre": "Drama",
            }
        }


class BaseUser(BaseModel):
    username : str = Field(..., max_length=50)
    password : str = Field(..., max_length=50)