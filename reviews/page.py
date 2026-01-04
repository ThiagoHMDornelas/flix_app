import streamlit as st
import pandas as pd
from components.grid import render_grid

from reviews.service import ReviewsService
from movies.service import MovieService


def show_reviews():
    review_service = ReviewsService()
    reviews = review_service.get_reviews()

    movie_service = MovieService()
    movies = movie_service.get_movies()

    # movies_dict_id_to_title = {movie['id']: movie['title'] for movie in movies} # dicionario usado no mapeamento
    movies_dict_title_to_id = {movie['title']: movie['id'] for movie in movies}  # dicionario usado no selectedbox

    if st.button('🔄 Atualizar Avaliações'):
        review_service.refresh_reviews()
        st.rerun()

    if reviews:
        # df = pd.json_normalize(reviews)
        # Desta forma. criando um dicionario
        # df['movie_title'] = df['movie'].map(movies_dict_id_to_title)
        # if 'movie' in df.columns:
        #     df = df.drop(columns=['movie'])

        # Faz o merge (join) entre reviews e movies
        df_reviews = pd.json_normalize(reviews)
        df_movies = pd.json_normalize(movies)
        df = pd.merge(
            df_reviews,                      # DataFrame da esquerda (reviews)
            df_movies[['id', 'title']],      # DataFrame da direita (só id e title)
            left_on='movie',                 # Coluna em df_reviews para fazer o join
            right_on='id',                   # Coluna em df_movies para fazer o join
            how='left'                       # Tipo de join (mantém todas as reviews)
        )

        # Renomeia as colunas para nomes claros
        df = df.rename(columns={
            'id_x': 'review_id',    # ID da review
            'id_y': 'movie_id',     # ID do filme (do merge)
            'title': 'movie_title'  # Título do filme
        })

        df = df.drop(columns=['movie_id'])

        render_grid(df, key="reviews_grid", title="Avaliações Cadastradas")
    else:
        st.warning('Nenhuma avaliação encontrada.')

    st.title('Cadastrar nova Avaliação')

    selected_movie_title = st.selectbox('Filme', list(movies_dict_title_to_id.keys()))

    stars = st.number_input(
        label='Estrelas',
        min_value=1,
        max_value=5,
        step=1,)
    comment = st.text_area('Comentário')

    # Mostra a mensagem se existir no session_state
    if 'success_message' in st.session_state:
        st.success(st.session_state.success_message)
        del st.session_state.success_message  # Remove após mostrar

    if 'error_message' in st.session_state:
        st.error(st.session_state.error_message)
        del st.session_state.error_message

    if st.button('Cadastrar'):
        try:
            new_review = review_service.create_review(
                movie_id=movies_dict_title_to_id[selected_movie_title],
                star=stars,
                comment=comment,
            )
            if new_review:
                st.session_state.success_message = f'Avaliação do filme {selected_movie_title} cadastrada com sucesso!'
                st.rerun()
            else:
                st.session_state.error_message = 'Não foi possível cadastrar a Avaliação'
                st.rerun()
        except Exception as e:
            st.session_state.error_message = f'Erro ao cadastrar a avaliação: {str(e)}'
            st.rerun()
