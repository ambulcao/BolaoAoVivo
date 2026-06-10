import streamlit as st

from utils.nav import home_page, palpites_page, meu_bolao_page

st.set_page_config(page_title="Bolão da Copa do Mundo 2026", page_icon="⚽", layout="wide")

st.session_state.setdefault("participant_id", None)
st.session_state.setdefault("participant_name", None)

pg = st.navigation([home_page, palpites_page, meu_bolao_page])
pg.run()
