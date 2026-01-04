import streamlit as st
import requests

from login.service import logout
from constants import BASE_URL


class MovieRepository:

    def __init__(self):
        self.__movies_url = f'{BASE_URL}movies/'
        self.__headers = {
            'Authorization': f'Bearer {st.session_state.token}'
        }

    def get_movies(self):
        response = requests.get(
            self.__movies_url,
            headers=self.__headers,
        )

        if response.status_code == 200:
            return response.json()
        if response.status_code == 401:  # token vencido
            logout()
            return None

        raise Exception(f'Erro ao obter dados da API. Status code: {response.status_code}')

    def create_movie(self, movie):
        response = requests.post(
            self.__movies_url,
            headers=self.__headers,
            data=movie,
        )

        if response.status_code == 201:
            return response.json()
        if response.status_code == 401:  # token vencido
            logout()
            return None

        raise Exception(f'Erro ao obter dados da API. Status code: {response.status_code}')

    def get_movie_stats(self):
        response = requests.get(
            f'{self.__movies_url}stats/',
            headers=self.__headers,
        )

        if response.status_code == 200:
            return response.json()
        if response.status_code == 401:  # token vencido
            logout()
            return None

        raise Exception(f'Erro ao obter dados da API. Status code: {response.status_code}')
