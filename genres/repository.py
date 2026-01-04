import streamlit as st
import requests

from login.service import logout
from constants import BASE_URL


class GenreRepository:

    def __init__(self):
        self.__genres_url = f'{BASE_URL}genres/'
        self.__headers = {
            'Authorization': f'Bearer {st.session_state.token}'
        }

    def get_genres(self):
        response = requests.get(
            self.__genres_url,
            headers=self.__headers,
        )

        if response.status_code == 200:
            return response.json()
        if response.status_code == 401:  # token vencido
            logout()
            return None

        raise Exception(f'Erro ao obter dados da API. Status code: {response.status_code}')

    def create_genre(self, genre):
        response = requests.post(
            self.__genres_url,
            headers=self.__headers,
            data=genre,
        )

        if response.status_code == 201:
            return response.json()
        if response.status_code == 401:  # token vencido
            logout()
            return None

        raise Exception(f'Erro ao obter dados da API. Status code: {response.status_code}')
