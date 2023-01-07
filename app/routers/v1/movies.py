"""Movies router."""
from http import HTTPStatus
from typing import Any, List, Union

from fastapi import APIRouter, Depends, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.middlewares.auth import JWTBearer
from app.config.database import Session
from app.models.movie import Movie as MovieORM
from app.routers.v1.models import Movie
from app.routers.v1.utils import (
    get_movie_by_id,
    get_movies_by_genre,
    get_movies_by_year,
)


router = APIRouter(
    prefix="/v1/movies",
    tags=["movies"],
)


MOVIES_MOCK = "app/routers/v1/mocks/movies.json"


@router.get("", status_code=HTTPStatus.OK, response_model=List[Movie])
def get_movies(genre: str = "", year: int = 1900, id: int = 0) -> List[Movie]:  # type: ignore
    """Get movies endpoint."""
    db = Session()
    movies = db.query(MovieORM).all()
    filtered_movies = []
    if genre:
        filtered_by_genre = get_movies_by_genre(genre, db)
        filtered_movies.append(filtered_by_genre)
    elif year:
        filtered_by_year = get_movies_by_year(year, db)
        filtered_movies.append(filtered_by_year)
    elif id:
        filtered_by_id = get_movie_by_id(id, db)
        filtered_movies.append(filtered_by_id)
    if filtered_movies and all(filtered_movies):
        return JSONResponse(  # type: ignore
            content=jsonable_encoder(filtered_movies), status_code=HTTPStatus.OK
        )
    if genre or year or id:
        response = {"error": "No movies found by the given criteria. Please try again"}
        return JSONResponse(content=response, status_code=HTTPStatus.NOT_FOUND)  # type: ignore

    return JSONResponse(content=jsonable_encoder(movies), status_code=HTTPStatus.OK)  # type: ignore


@router.post(
    "",
    status_code=HTTPStatus.CREATED,
    response_model=dict,
    dependencies=[Depends(JWTBearer())],
)
def create_movie(movie: Movie) -> dict:
    """Create movie endpoint.

    Args:
        movie (Movie): Movie object.

    Returns:
        dict: Response message.
    """
    db = Session()
    new_movie = MovieORM(**movie.dict())
    db.add(new_movie)
    db.commit()

    response = {"message": "Movie created successfully"}
    return JSONResponse(content=response, status_code=HTTPStatus.CREATED)  # type: ignore


@router.put("/{movie_id}", status_code=HTTPStatus.OK, response_model=dict, dependencies=[Depends(JWTBearer())])
def update_movie(movie_id: int, movie: Movie) -> Union[Any, JSONResponse]:
    """Update movie endpoint.

    Args:
        movie_id (int): Movie id.
        movie (Movie): Movie object.

    Returns:
        Union[Any, JSONResponse]: Response message.
    """

    db = Session()
    result = get_movie_by_id(movie_id, db)

    if isinstance(result, JSONResponse):
        return result

    result.title = movie.title
    result.overview = movie.overview
    result.year = movie.year
    result.rating = movie.rating
    result.genre = movie.genre
    db.commit()

    response = {"message": "Movie updated successfully"}
    return JSONResponse(content=response, status_code=HTTPStatus.OK)


@router.delete("/{movie_id}", status_code=HTTPStatus.NO_CONTENT, dependencies=[Depends(JWTBearer())])
def delete_movie(movie_id: int) -> Response:
    """Delete movie endpoint.

    Args:
        movie_id (int): Movie id.

    Returns:
        Response: Response message.
    """

    db = Session()
    result = get_movie_by_id(movie_id, db)

    if isinstance(result, JSONResponse):
        return result

    db.delete(result)
    db.commit()

    return Response(status_code=HTTPStatus.NO_CONTENT)
