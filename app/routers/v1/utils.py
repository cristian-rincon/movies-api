from http import HTTPStatus

from fastapi.responses import JSONResponse

from app.config.database import Session
from app.models.movie import Movie as MovieORM


def get_movies_by_genre(genre: str, db: Session):
    return db.query(MovieORM).filter(MovieORM.genre.contains(genre)).all()


def get_movies_by_year(year: int, db: Session):
    return db.query(MovieORM).filter(MovieORM.year == year).all()


def get_movie_by_id(movie_id: int, db: Session):
    if movie_found := db.query(MovieORM).filter(MovieORM.id == movie_id).first():
        return movie_found

    response = {"error": "Movie not found"}
    return JSONResponse(content=response, status_code=HTTPStatus.NOT_FOUND)
