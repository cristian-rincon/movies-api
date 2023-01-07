"""Api utils."""

from http import HTTPStatus
from typing import Any

from fastapi.responses import JSONResponse

from app.config.database import Session
from app.models.movie import Movie as MovieORM


def get_movies_by_genre(genre: str, db: Session) -> Any:
    """Get movies by genre.

    Args:
        genre (str): Movie genre.
        db (Session): Database session.

    """
    return db.query(MovieORM).filter(MovieORM.genre.contains(genre)).all()


def get_movies_by_year(year: int, db: Session) -> Any:
    """Get movies by year.

    Args:
        year (int): Movie year.
        db (Session): Database session.

    """

    return db.query(MovieORM).filter(MovieORM.year == year).all()


def get_movie_by_id(movie_id: int, db: Session) -> Any:
    """Get movie by id.

    Args:

        movie_id (int): Movie id.
        db (Session): Database session.

    """

    if movie_found := db.query(MovieORM).filter(MovieORM.id == movie_id).first():
        return movie_found

    response = {"error": "Movie not found"}
    return JSONResponse(content=response, status_code=HTTPStatus.NOT_FOUND)
