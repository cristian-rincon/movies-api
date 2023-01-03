import json
from fastapi import APIRouter

from app.routers.v1.models import Movie
from app.routers.v1.utils import (
    get_movies_by_genre,
    get_movies_by_year,
    get_movie_by_id,
    movies,
)

router = APIRouter(
    prefix="/v1/movies",
    tags=["movies"],
)


@router.get("")
def get_movies(genre: str = None, year: int = None, id: int = None):
    if genre:
        return get_movies_by_genre(genre)
    elif year:
        return get_movies_by_year(year)
    elif id:
        return get_movie_by_id(id)

    return movies


@router.post("")
def create_movie(movie: Movie):
    if movie.id in [movie["id"] for movie in movies]:
        return {"error": "Movie already exists"}
    movies.append(movie.dict())
    with open("app/routers/v1/mocks/movies.json", "w") as f:
        json.dump(movies, f)
    return movies


@router.put("/{movie_id}")
def update_movie(movie_id: int, movie: Movie):
    idx, _ = get_movie_by_id(movie_id, get_index=True)
    movies[idx] = movie.dict()

    with open("app/routers/v1/mocks/movies.json", "w") as f:
        json.dump(movies, f)

    return movies


@router.delete("/{movie_id}")
def delete_movie(movie_id: int):
    idx, _ = get_movie_by_id(movie_id, get_index=True)
    movies.pop(idx)
    with open("app/routers/v1/mocks/movies.json", "w") as f:
        json.dump(movies, f)
    return movies
