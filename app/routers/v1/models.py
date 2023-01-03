from typing import Union
from pydantic import BaseModel, Field

class Movie(BaseModel):
    id: int = Field(...)
    title: str
    overview: str
    year: int
    rating: Union[int, float]
    genre: str