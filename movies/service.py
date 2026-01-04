import streamlit as st

from movies.repository import MovieRepository


@st.cache_data(ttl=120)  # Cache por 2 minutos
def _get_movies_cached():
    repository = MovieRepository()
    return repository.get_movies()


class MovieService:

    def __init__(self):
        self.movie_repository = MovieRepository()

    def get_movies(self):
        return _get_movies_cached()

    def create_movie(self, title, genre, release_date, actors, resume):
        movie = dict(
            title=title,
            genre=genre,
            release_date=release_date,
            actors=actors,
            resume=resume
        )
        new_movie = self.movie_repository.create_movie(movie)
        _get_movies_cached.clear()

        return new_movie

    def get_movie_stats(self):
        return self.movie_repository.get_movie_stats()

    def refresh_movies(self):
        _get_movies_cached.clear()
        return self.get_movies()
