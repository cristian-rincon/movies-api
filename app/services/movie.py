from typing import Union
from app.config.database import Session
from app.models.movie import Movie as MovieORM

from app.routers.v1.utils import (
    get_movie_by_id,
    get_movies_by_genre,
    get_movies_by_year,
)

class MovieService:
    def __init__(self, database: Session):
        """Movie service."""
        self.database = database

    def get_movies(self, genre: Union[str, None] = None, year: Union[int, None] = None, id: Union[int, None] = None) -> tuple:
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

    def create_movie(self, movie: MovieORM) -> None:
        """Create movie endpoint.

        Args:
            movie (Movie): Movie object.
        """
        self.database.add(movie)
        self.database.commit()