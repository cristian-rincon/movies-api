import json

def retrieve_movies():
    with open("app/routers/v1/mocks/movies.json", "r") as f:
        movies = json.load(f)
    return movies

movies = retrieve_movies()

def get_movies_by_genre(genre: str):
    movies_by_genre = []
    for movie in movies:
        genres = list(movie["genre"].split("|"))
        if genre.capitalize() in genres:
            movies_by_genre.append(movie)
    return movies_by_genre


def get_movies_by_year(year: int):
    return [movie for movie in movies if movie["year"] == year]


def get_movie_by_id(movie_id: int, get_index=False):
    for index, movie in enumerate(movies):
        if movie["id"] == movie_id:
            return (index, movie) if get_index else movie