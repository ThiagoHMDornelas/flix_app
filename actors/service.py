import streamlit as st

from actors.repository import ActorRepository


@st.cache_data(ttl=120)  # Cache por 2 minutos
def _get_actors_cached():
    repository = ActorRepository()
    return repository.get_actors()


class ActorService:

    def __init__(self):
        self.actor_repository = ActorRepository()

    def get_actors(self):
        return _get_actors_cached()

    def create_actor(self, name, birthday, nationality):
        actor = dict(
            name=name,
            birthday=birthday,
            nationality=nationality,
        )
        new_actor = self.actor_repository.create_actor(actor)
        _get_actors_cached.clear()

        return new_actor

    def refresh_actors(self):
        _get_actors_cached.clear()
        return self.get_actors()
