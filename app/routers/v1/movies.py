"""Movies router."""
from http import HTTPStatus
from typing import Any, List, Union

from fastapi import APIRouter, Depends, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.config.oauth2 import get_current_user
from app.config.database import Session, get_db
from app.schemas.user import User as UserSchema
from app.schemas.movie import Movie
from app.services.movie import MovieService


router = APIRouter(
    prefix="/v1/movies",
    tags=["movies"],
)


MOVIES_MOCK = "app/routers/v1/mocks/movies.json"


@router.get("", status_code=HTTPStatus.OK, response_model=List[Movie])
def get_movies(
    database: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user),
    genre: Union[str, None] = None,
    year: Union[int, None] = None,
    id: Union[int, None] = None,
) -> List[Movie]:  # type: ignore
    """Get movies endpoint."""
    _ = current_user
    movie_service = MovieService(database)
    movies, filtered_movies = movie_service.get_movies(genre, year, id)

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
)
def create_movie(
    movie: Movie,
    database: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user),
) -> dict:
    """Create movie endpoint.

    Args:
        movie (Movie): Movie object.

    Returns:
        dict: Response message.
    """
    _ = current_user
    movie_service = MovieService(database)
    movie_service.create_movie(movie)

    response = {"message": "Movie created successfully"}
    return JSONResponse(content=response, status_code=HTTPStatus.CREATED)  # type: ignore


@router.put(
    "/{movie_id}",
    status_code=HTTPStatus.OK,
    response_model=dict,
)
def update_movie(
    movie_id: int,
    movie: Movie,
    database: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user),
) -> Union[Any, JSONResponse]:
    """Update movie endpoint.

    Args:
        movie_id (int): Movie id.
        movie (Movie): Movie object.

    Returns:
        Union[Any, JSONResponse]: Response message.
    """

    _ = current_user
    movie_service = MovieService(database)
    movie_service.update_movie(movie, movie_id)

    response = {"message": "Movie updated successfully"}
    return JSONResponse(content=response, status_code=HTTPStatus.OK)


@router.delete(
    "/{movie_id}",
    status_code=HTTPStatus.NO_CONTENT,
)
def delete_movie(
    movie_id: int,
    database: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user),
) -> Response:
    """Delete movie endpoint.

    Args:
        movie_id (int): Movie id.

    Returns:
        Response: Response message.
    """

    _ = current_user
    movie_service = MovieService(database)
    movie_service.delete_movie(movie_id)

    return Response(status_code=HTTPStatus.NO_CONTENT)
