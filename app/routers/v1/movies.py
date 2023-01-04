import json
from typing import List
from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse
from http import HTTPStatus

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


MOVIES_MOCK = "app/routers/v1/mocks/movies.json"


@router.get("", status_code=HTTPStatus.OK, response_model=List[Movie])
def get_movies(genre: str = None, year: int = None, id: int = None) -> List[Movie]:
    filtered_movies = []
    if genre:
        filtered_by_genre = get_movies_by_genre(genre)
        filtered_movies.append(filtered_by_genre)
    elif year:
        filtered_by_year = get_movies_by_year(year)
        filtered_movies.append(filtered_by_year)
    elif id:
        filtered_by_id = get_movie_by_id(id)
        filtered_movies.append(filtered_by_id)
    if filtered_movies and all(filtered_movies):
        return JSONResponse(content=filtered_movies, status_code=HTTPStatus.OK)
    elif genre or year or id:
        response = {"error": "No movies found by the given criteria. Please try again"}
        return JSONResponse(content=response, status_code=HTTPStatus.NOT_FOUND)

    return JSONResponse(content=movies, status_code=HTTPStatus.OK)


@router.post("", status_code=HTTPStatus.CREATED, response_model=dict)
def create_movie(movie: Movie) -> dict:
    if movie.id in [movie["id"] for movie in movies]:
        return {"error": "Movie already exists"}
    movies.append(movie.dict())
    with open(MOVIES_MOCK, "w") as f:
        json.dump(movies, f)
    response = {"message": "Movie created successfully"}
    return JSONResponse(content=response, status_code=HTTPStatus.CREATED)


@router.put("/{movie_id}", status_code=HTTPStatus.OK, response_model=dict)
def update_movie(movie_id: int, movie: Movie) -> dict:
    try:
        idx, _ = get_movie_by_id(movie_id, get_index=True)
        movies[idx] = movie.dict()
    except Exception:
        response = {"error": "Movie not found"}
        return JSONResponse(content=response, status_code=HTTPStatus.NOT_FOUND)
    else:
        with open(MOVIES_MOCK, "w") as f:
            json.dump(movies, f)

        response = {"message": "Movie updated successfully"}
        return JSONResponse(content=response, status_code=HTTPStatus.OK)


@router.delete("/{movie_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_movie(movie_id: int) -> Response:
    idx, _ = get_movie_by_id(movie_id, get_index=True)
    movies.pop(idx)
    with open(MOVIES_MOCK, "w") as f:
        json.dump(movies, f)

    return Response(status_code=HTTPStatus.NO_CONTENT)
