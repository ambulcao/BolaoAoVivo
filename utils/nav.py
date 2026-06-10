import streamlit as st

home_page = st.Page("app_pages/home.py", title="Início", icon="⚽", default=True)
palpites_page = st.Page("app_pages/palpites.py", title="Palpites", icon="📝")
meu_bolao_page = st.Page("app_pages/meu_bolao.py", title="Meu Bolão", icon="🏆")
