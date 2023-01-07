"""Movie service."""

from typing import Any, Union
from fastapi.responses import JSONResponse
from app.config.database import Session
from app.models.movie import Movie as MovieORM
from app.schemas.movie import Movie

from app.routers.v1.utils import (
    get_movie_by_id,
    get_movies_by_genre,
    get_movies_by_year,
)


class MovieService:
    """Movie service Class.

    Builtin methods:
        get_movies: Get movies endpoint.
        create_movie: Create movie endpoint.
        update_movie: Update movie endpoint.
        delete_movie: Delete movie endpoint.
    """

    def __init__(self, database: Session):
        """Movie service."""
        self.database = database

    def get_movies(
        self,
        genre: Union[str, None] = None,
        year: Union[int, None] = None,
        id: Union[int, None] = None,
    ) -> tuple:
        """Get movies endpoint. If no filters are provided, return all movies.

        Args:
            genre (str): Movie genre.
            year (int): Movie year.
            id (int): Movie id.

        Returns:
            tuple: Movies and filtered movies.
        """
        movies = self.database.query(MovieORM).all()
        filtered_movies = []
        if genre:
            filtered_by_genre = get_movies_by_genre(genre, self.database)
            filtered_movies.append(filtered_by_genre)
        elif year:
            filtered_by_year = get_movies_by_year(year, self.database)
            filtered_movies.append(filtered_by_year)
        elif id:
            filtered_by_id = get_movie_by_id(id, self.database)
            filtered_movies.append(filtered_by_id)

        return movies, filtered_movies

    def create_movie(self, movie: Movie) -> None:
        """Create movie endpoint.

        Args:
            movie (Movie): Movie object.
        """
        new_movie = MovieORM(**movie.dict())
        self.database.add(new_movie)
        self.database.commit()

    def update_movie(self, movie: Movie, id: int) -> Union[Any, None]:
        """Update movie endpoint.

        Args:
            movie (Movie): Movie object.
            id (int): Movie id.
        """
        result = get_movie_by_id(id, self.database)

        if isinstance(result, JSONResponse):
            return result

        result.title = movie.title
        result.overview = movie.overview
        result.year = movie.year
        result.rating = movie.rating
        result.genre = movie.genre
        self.database.commit()
        return None

    def delete_movie(self, id: int) -> Union[Any, None]:
        """Delete movie endpoint.

        Args:
            id (int): Movie id.
        """
        result = get_movie_by_id(id, self.database)

        if isinstance(result, JSONResponse):
            return result

        self.database.delete(result)
        self.database.commit()
        return None
