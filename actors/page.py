import streamlit as st
import pandas as pd
from components.grid import render_grid
from datetime import datetime

from actors.service import ActorService
from constants import NATIONALITY_CHOICES, NATIONALITY_DISPLAY


def show_actors():
    actor_service = ActorService()
    actors = actor_service.get_actors()

    if st.button('🔄 Atualizar atores'):
        actor_service.refresh_actors()
        st.rerun()

    if actors:
        df = pd.json_normalize(actors)

        # Converte os códigos de nacionalidade para nomes legíveis
        if 'nationality' in df.columns:
            df['nationality'] = df['nationality'].map(NATIONALITY_DISPLAY)
        if 'birthday' in df.columns:
            df['birthday'] = pd.to_datetime(df['birthday']).dt.strftime('%d/%m/%Y')

        render_grid(df, key="actors_grid", title="Lista de Atores / Atrizes")
    else:
        st.warning('Nenhum ator/atriz encontrado(a).')

    st.title('Cadastrar novo Ator/Atriz')

    name = st.text_input('Nome do Ator')
    birthday = st.date_input(
        label='Data de Aniversário',
        value=datetime.today(),
        min_value=datetime(1600, 1, 1).date(),
        max_value=datetime.today(),
        format='DD/MM/YYYY'
    )
    nationality = st.selectbox(
        label='Nacionalidade',
        options=NATIONALITY_CHOICES.keys(),  # Usa o dicionário para o selectbox
    )

    # Mostra a mensagem se existir no session_state
    if 'success_message' in st.session_state:
        st.success(st.session_state.success_message)
        del st.session_state.success_message  # Remove após mostrar

    if 'error_message' in st.session_state:
        st.error(st.session_state.error_message)
        del st.session_state.error_message

    if st.button('Cadastrar'):
        if not name or not name.strip():
            st.error('Por favor, informe o nome do Ator/Atriz!')
        else:
            try:
                # Converte o nome exibido para o código do banco
                nationality_code = NATIONALITY_CHOICES[nationality]

                new_actor = actor_service.create_actor(
                    name=name,
                    birthday=birthday,
                    nationality=nationality_code,
                )
                if new_actor:
                    st.session_state.success_message = f'Ator/Atriz {name} cadastrado(a) com sucesso!'
                    st.rerun()
                else:
                    st.session_state.error_message = 'Não foi possível cadastrar o Ator/Atriz.'
                    st.rerun()
            except Exception as e:
                st.session_state.error_message = f'Erro ao cadastrar ator/atriz: {str(e)}'
                st.rerun()
