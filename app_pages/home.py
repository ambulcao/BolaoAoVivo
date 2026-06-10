import streamlit as st

from utils.db import get_or_create_participant
from utils.nav import palpites_page, meu_bolao_page

st.markdown(
    """
    <div style="background-color:#1a7f37;padding:1.2rem;border-radius:8px;margin-bottom:1rem;">
        <h1 style="color:white;text-align:center;margin:0;">⚽ Bolão da Copa do Mundo 2026</h1>
        <p style="color:white;text-align:center;margin:0;">Faça seus palpites para a fase de grupos!</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if st.session_state["participant_id"]:
    st.success(f"Você está participando como **{st.session_state['participant_name']}**.")
    st.write("Use o menu à esquerda para fazer seus palpites e ver o resumo do seu bolão.")
    st.page_link(palpites_page, label="Fazer/editar palpites")
    st.page_link(meu_bolao_page, label="Meu bolão")

    if st.button("Sair / trocar participante"):
        st.session_state["participant_id"] = None
        st.session_state["participant_name"] = None
        st.rerun()
else:
    st.subheader("Cadastro do participante")
    st.write(
        "Preencha seus dados para participar. Se o seu email já estiver cadastrado, "
        "vamos recuperar seus palpites anteriores."
    )

    with st.form("cadastro_form"):
        name = st.text_input("Nome")
        phone = st.text_input("Telefone")
        email = st.text_input("Email")
        submitted = st.form_submit_button("Entrar no bolão")

    if submitted:
        if not name.strip() or not phone.strip() or not email.strip():
            st.error("Preencha nome, telefone e email para continuar.")
        else:
            participant = get_or_create_participant(name, phone, email)
            st.session_state["participant_id"] = participant["id"]
            st.session_state["participant_name"] = participant["name"]
            st.rerun()
