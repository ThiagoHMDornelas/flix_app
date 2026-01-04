import streamlit as st
import pandas as pd
from components.grid import render_grid
from datetime import datetime

from movies.service import MovieService
from actors.service import ActorService
from genres.service import GenreService


def show_movies():
    movie_service = MovieService()
    movies = movie_service.get_movies()

    if st.button('🔄 Atualizar filmes'):
        movie_service.refresh_movies()
        st.rerun()

    if movies:
        df = pd.json_normalize(movies)

        if 'release_date' in df.columns:
            df['release_date'] = pd.to_datetime(df['release_date']).dt.strftime('%d/%m/%Y')

        df = df.drop(columns=['actors', 'genre.id'])
        render_grid(df, key="movies_grid", title="Lista de Filmes")
    else:
        st.warning('Nenhum filme encontrado.')

    st.title('Cadastrar novo Filme')

    title = st.text_input('Título do Filme')
    release_date = st.date_input(
        label='Data de Lançamento',
        value=datetime.today(),
        min_value=datetime(1600, 1, 1).date(),
        max_value=datetime.today(),
        format='DD/MM/YYYY'
    )

    genre_service = GenreService()
    genres = genre_service.get_genres()
    genre_names = {genre['name']: genre['id'] for genre in genres}
    selected_genre_name = st.selectbox('Gênero', list(genre_names.keys()))

    actor_service = ActorService()
    actors = actor_service.get_actors()
    actor_names = {actor['name']: actor['id'] for actor in actors}
    selected_actor_names = st.multiselect('Atores/Atrizes', list(actor_names.keys()))
    actors_code = [actor_names[name] for name in selected_actor_names]

    resume = st.text_area('Resumo')

    # Mostra a mensagem se existir no session_state
    if 'success_message' in st.session_state:
        st.success(st.session_state.success_message)
        del st.session_state.success_message  # Remove após mostrar

    if 'error_message' in st.session_state:
        st.error(st.session_state.error_message)
        del st.session_state.error_message

    if st.button('Cadastrar'):
        if not title or not title.strip():
            st.error('Por favor, informe o nome do Filme!')
        else:
            try:
                new_movie = movie_service.create_movie(
                    title=title,
                    genre=genre_names[selected_genre_name],
                    release_date=release_date,
                    actors=actors_code,
                    resume=resume,
                )
                if new_movie:
                    st.session_state.success_message = f'Filme {title} cadastrado com sucesso!'
                    st.rerun()
                else:
                    st.session_state.error_message = 'Não foi possível cadastrar o Filme'
                    st.rerun()
            except Exception as e:
                st.session_state.error_message = f'Erro ao cadastrar filme: {str(e)}'
                st.rerun()
