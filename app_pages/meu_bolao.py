import streamlit as st

from utils.bracket import STAGE_NAMES, build_round_of_32, simulate_bracket
from utils.db import get_groups_with_teams, get_predictions
from utils.nav import palpites_page, home_page

if not st.session_state.get("participant_id"):
    st.warning("Você precisa se cadastrar antes de ver seu bolão.")
    st.page_link(home_page, label="⬅️ Voltar para o cadastro")
    st.stop()

st.title("🏆 Meu Bolão")

groups = get_groups_with_teams()
picks = get_predictions(st.session_state["participant_id"])

teams_by_id = {team["id"]: team for group in groups for team in group["teams"]}

if not picks:
    st.info("Você ainda não salvou nenhum palpite.")
    st.page_link(palpites_page, label="Fazer palpites")
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

if len(picks) < len(groups):
    st.info(
        "Complete os palpites de todos os 12 grupos para gerar o seu chaveamento "
        "completo, da Rodada de 32 até o campeão."
    )
    st.page_link(palpites_page, label="Fazer palpites")
else:
    st.caption(
        "Chaveamento gerado a partir dos seus palpites de grupo. Os 8 melhores "
        "terceiros colocados (sorteio único, válido para todos os participantes) e "
        "os vencedores de cada fase são sorteados automaticamente."
    )

    round_of_32 = build_round_of_32(groups, picks)
    rounds, winners_per_round, champion = simulate_bracket(
        st.session_state["participant_id"], round_of_32
    )

    def team_box(team, is_winner):
        style = (
            "border:1px solid #1a7f37;background-color:#eaf5ec;font-weight:600;"
            if is_winner
            else "border:1px solid #ddd;color:#666;"
        )
        return (
            f"<div style='{style}border-radius:6px;padding:4px 8px;"
            f"margin-bottom:4px;font-size:0.85em;'>{team['flag_emoji']} {team['name']}</div>"
        )

    bracket_cols = st.columns(len(rounds))
    for col, stage, matches, winners in zip(bracket_cols, STAGE_NAMES, rounds, winners_per_round):
        with col:
            st.markdown(f"**{stage}**")
            for match, winner in zip(matches, winners):
                team_a, team_b = match
                st.markdown(team_box(team_a, team_a == winner), unsafe_allow_html=True)
                st.markdown(team_box(team_b, team_b == winner), unsafe_allow_html=True)
                st.markdown("<div style='margin-bottom:10px;'></div>", unsafe_allow_html=True)

    st.divider()
    st.markdown(
        f"""
        <div style="background-color:#1a7f37;padding:1rem;border-radius:8px;text-align:center;">
            <span style="color:white;font-size:1.1em;">🏆 Campeão</span><br>
            <span style="color:white;font-size:1.5em;font-weight:700;">
                {champion['flag_emoji']} {champion['name']}
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )
