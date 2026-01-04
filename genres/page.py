import streamlit as st
import pandas as pd
from components.grid import render_grid

from genres.service import GenreService


def show_genres():
    genre_service = GenreService()
    genres = genre_service.get_genres()

    if st.button('🔄 Atualizar gêneros'):
        genre_service.refresh_genres()
        st.rerun()

    if genres:
        # df = pd.DataFrame(genres)
        df = pd.json_normalize(genres)
        render_grid(df, key="genres_grid", title="Lista de Gêneros")
    else:
        st.warning('Nenhum gênero encontrado.')

    st.title('Cadastrar novo Gênero')

    name = st.text_input('Nome do Gênero')

    # Mostra a mensagem se existir no session_state
    if 'success_message' in st.session_state:
        st.success(st.session_state.success_message)
        del st.session_state.success_message  # Remove após mostrar

    if 'error_message' in st.session_state:
        st.error(st.session_state.error_message)
        del st.session_state.error_message

    if st.button('Cadastrar'):
        if not name or not name.strip():
            st.error('Por favor, informe o nome do gênero!')
        else:
            try:
                new_genre = genre_service.create_genres(name=name)
                if new_genre:
                    st.session_state.success_message = f'Gênero {name} cadastrado com sucesso!'
                    st.rerun()
                else:
                    st.session_state.error_message = 'Não foi possível cadastrar o gênero.'
                    st.rerun()
            except Exception as e:
                st.session_state.error_message = f'Erro ao cadastrar gênero: {str(e)}'
                st.rerun()
