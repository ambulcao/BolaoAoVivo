import streamlit as st

from utils.db import get_groups_with_teams, get_predictions, save_predictions
from utils.nav import home_page

if not st.session_state.get("participant_id"):
    st.warning("Você precisa se cadastrar antes de fazer seus palpites.")
    st.page_link(home_page, label="⬅️ Voltar para o cadastro")
    st.stop()

st.title("📝 Palpites - Fase de Grupos")
st.caption(
    "Escolha o 1º e o 2º colocado de cada grupo. "
    "Os 8 melhores terceiros colocados serão sorteados automaticamente."
)

groups = get_groups_with_teams()
saved_picks = get_predictions(st.session_state["participant_id"])

with st.form("palpites_form"):
    new_picks: dict[str, dict[str, int]] = {}
    cols = st.columns(3)

    for i, group in enumerate(groups):
        col = cols[i % 3]
        with col:
            with st.container(border=True):
                st.markdown(f"**Grupo {group['id']}**")
                teams = group["teams"]
                options = [team["id"] for team in teams]
                labels = {team["id"]: f"{team['flag_emoji']} {team['name']}" for team in teams}

                for team in teams:
                    st.write(f"{team['flag_emoji']} {team['name']}")

                saved = saved_picks.get(group["id"], {})
                first_default = saved.get("first_team_id", options[0])
                second_default = saved.get("second_team_id", options[1])

                first_idx = options.index(first_default) if first_default in options else 0
                second_idx = options.index(second_default) if second_default in options else 1

                first_team = st.selectbox(
                    "1º colocado",
                    options=options,
                    index=first_idx,
                    format_func=lambda tid: labels[tid],
                    key=f"first_{group['id']}",
                )
                second_team = st.selectbox(
                    "2º colocado",
                    options=options,
                    index=second_idx,
                    format_func=lambda tid: labels[tid],
                    key=f"second_{group['id']}",
                )

                new_picks[group["id"]] = {
                    "first_team_id": first_team,
                    "second_team_id": second_team,
                }

    submitted = st.form_submit_button("💾 Salvar palpites", type="primary")

if submitted:
    invalid_groups = [
        g for g, pick in new_picks.items()
        if pick["first_team_id"] == pick["second_team_id"]
    ]
    if invalid_groups:
        st.error(
            "O 1º e o 2º colocado não podem ser o mesmo time nos grupos: "
            + ", ".join(invalid_groups)
        )
    else:
        save_predictions(st.session_state["participant_id"], new_picks)
        st.success("Palpites salvos com sucesso!")
