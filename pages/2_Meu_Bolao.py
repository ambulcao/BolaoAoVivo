import streamlit as st

from utils.db import get_groups_with_teams, get_predictions

st.set_page_config(page_title="Meu Bolão - Bolão 2026", page_icon="🏆", layout="wide")

if not st.session_state.get("participant_id"):
    st.warning("Você precisa se cadastrar antes de ver seu bolão.")
    st.page_link("streamlit_app.py", label="⬅️ Voltar para o cadastro")
    st.stop()

st.title("🏆 Meu Bolão")

groups = get_groups_with_teams()
picks = get_predictions(st.session_state["participant_id"])

teams_by_id = {team["id"]: team for group in groups for team in group["teams"]}

if not picks:
    st.info("Você ainda não salvou nenhum palpite.")
    st.page_link("pages/1_Palpites.py", label="📝 Fazer palpites")
else:
    st.subheader("Seus palpites por grupo")

    cols = st.columns(3)
    for i, group in enumerate(groups):
        col = cols[i % 3]
        pick = picks.get(group["id"])
        with col:
            with st.container(border=True):
                st.markdown(f"**Grupo {group['id']}**")
                if pick:
                    first = teams_by_id.get(pick["first_team_id"])
                    second = teams_by_id.get(pick["second_team_id"])
                    st.write(f"🥇 1º: {first['flag_emoji']} {first['name']}")
                    st.write(f"🥈 2º: {second['flag_emoji']} {second['name']}")
                else:
                    st.write("Sem palpite ainda.")

st.divider()

st.subheader("Mata-mata")
st.caption(
    "Estrutura ilustrativa do mata-mata. Os confrontos reais dependerão do "
    "resultado da fase de grupos e do sorteio dos 8 melhores terceiros colocados."
)

round_of_32 = [
    "1º A vs 2º B", "1º C vs 2º D", "1º E vs 2º F", "1º G vs 2º H",
    "1º I vs 2º J", "1º K vs 2º L", "1º B vs 3º (melhor)", "1º D vs 3º (melhor)",
    "1º F vs 3º (melhor)", "1º H vs 3º (melhor)", "1º J vs 3º (melhor)", "1º L vs 3º (melhor)",
    "2º A vs 2º C", "2º E vs 2º G", "2º I vs 2º K", "3º (melhor) vs 3º (melhor)",
]

bracket_cols = st.columns(4)
stage_names = ["Rodada de 32", "Oitavas de Final", "Quartas de Final", "Semifinal / Final"]
stage_sizes = [16, 8, 4, 2]

for col, stage, size in zip(bracket_cols, stage_names, stage_sizes):
    with col:
        st.markdown(f"**{stage}**")
        if stage == "Rodada de 32":
            for matchup in round_of_32:
                st.markdown(f"<div style='border:1px solid #ddd;border-radius:6px;padding:4px 8px;margin-bottom:6px;font-size:0.85em;'>{matchup}</div>", unsafe_allow_html=True)
        else:
            for n in range(size):
                st.markdown(f"<div style='border:1px solid #ddd;border-radius:6px;padding:4px 8px;margin-bottom:6px;font-size:0.85em;color:#999;'>A definir</div>", unsafe_allow_html=True)
