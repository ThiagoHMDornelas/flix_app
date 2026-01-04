import streamlit as st

from genres.repository import GenreRepository


@st.cache_data(ttl=120)  # Cache por 2 minutos
def _get_genres_cached():
    repository = GenreRepository()
    return repository.get_genres()


class GenreService:

    def __init__(self):
        self.genre_repository = GenreRepository()

    def get_genres(self):
        return _get_genres_cached()

    def create_genres(self, name):
        genre = dict(
            name=name,
        )
        new_genre = self.genre_repository.create_genre(genre)
        _get_genres_cached.clear()

        return new_genre

    def refresh_genres(self):
        _get_genres_cached.clear()
        return self.get_genres()
