"""Movie model for ORM."""

from sqlalchemy import Column, Integer, String

from app.config.database import Base


class Movie(Base):
    """Movie model.

    Attributes:
        id (int): Movie id. Primary key. Autoincrement. Index.
        title (str): Movie title.
        overview (str): Movie overview.
        year (int): Movie year.
        rating (int): Movie rating.
        genre (str): Movie genre.
    """

    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    overview = Column(String)
    year = Column(Integer)
    rating = Column(Integer)
    genre = Column(String)
