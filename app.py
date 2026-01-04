from streamlit_option_menu import option_menu
import streamlit as st

from login.page import show_login
from genres.page import show_genres
from actors.page import show_actors
from movies.page import show_movies
from reviews.page import show_reviews
from home.page import show_home


def main():
    if 'token' not in st.session_state:
        show_login()
    else:
        st.title('Flix App')

        with st.sidebar:
            selected = option_menu(
                "Meu Sistema",
                ["Início", "Gêneros", "Atores/Atrizes", "Filmes", "Avaliações"],
                icons=["bar-chart", "file-earmark-text", "person", "film", "star"],
                menu_icon="cast",
                default_index=0
            )

        # ===== LIMPA CACHE AO TROCAR DE PÁGINA =====
        # Armazena a página anterior
        if 'previous_page' not in st.session_state:
            st.session_state.previous_page = selected

        # Se mudou de página, limpa os caches
        if st.session_state.previous_page != selected:
            st.cache_data.clear()  # Limpa TODOS os caches
            st.session_state.previous_page = selected

        # ===== FIM DA LIMPEZA =====

        if selected == 'Início':
            show_home()

        if selected == 'Gêneros':
            show_genres()

        if selected == 'Atores/Atrizes':
            show_actors()

        if selected == 'Filmes':
            show_movies()

        if selected == 'Avaliações':
            show_reviews()


if __name__ == '__main__':
    main()
