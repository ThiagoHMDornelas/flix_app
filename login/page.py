import streamlit as st
from login.service import login


def show_login():
    st.title('Login')

    with st.form("login_form", clear_on_submit=False):
        username = st.text_input('Usuário')
        password = st.text_input(
            'Senha',
            type='password'
        )

        submitted = st.form_submit_button('Login')

        if submitted:
            if not username or not password:
                st.warning("Preencha usuário e senha")
            else:
                login(
                    username=username,
                    password=password
                )
