import streamlit as st

from utils.supabase_client import get_supabase


@st.cache_data(ttl=3600)
def get_groups_with_teams():
    """Retorna os 12 grupos, cada um com seus 4 times ordenados."""
    sb = get_supabase()
    groups = sb.table("groups").select("id, name").order("id").execute().data
    teams = (
        sb.table("teams")
        .select("id, group_id, name, flag_emoji, position")
        .order("group_id")
        .order("position")
        .execute()
        .data
    )

    teams_by_group = {}
    for team in teams:
        teams_by_group.setdefault(team["group_id"], []).append(team)

    for group in groups:
        group["teams"] = teams_by_group.get(group["id"], [])

    return groups


def get_or_create_participant(name: str, phone: str, email: str) -> dict:
    """Busca um participante pelo email ou cria um novo."""
    sb = get_supabase()
    email = email.strip().lower()

    existing = (
        sb.table("participants").select("*").eq("email", email).execute().data
    )
    if existing:
        return existing[0]

    created = (
        sb.table("participants")
        .insert({"name": name.strip(), "phone": phone.strip(), "email": email})
        .execute()
        .data
    )
    return created[0]


def save_predictions(participant_id: str, picks: dict[str, dict[str, int]]):
    """Salva os palpites do participante.

    `picks` é um dict {group_id: {"first_team_id": int, "second_team_id": int}}.
    """
    sb = get_supabase()
    rows = [
        {
            "participant_id": participant_id,
            "group_id": group_id,
            "first_team_id": pick["first_team_id"],
            "second_team_id": pick["second_team_id"],
        }
        for group_id, pick in picks.items()
    ]
    sb.table("predictions").upsert(rows, on_conflict="participant_id,group_id").execute()


def get_predictions(participant_id: str) -> dict[str, dict[str, int]]:
    """Retorna os palpites já salvos como {group_id: {"first_team_id":..., "second_team_id":...}}."""
    sb = get_supabase()
    rows = (
        sb.table("predictions")
        .select("group_id, first_team_id, second_team_id")
        .eq("participant_id", participant_id)
        .execute()
        .data
    )
    return {
        row["group_id"]: {
            "first_team_id": row["first_team_id"],
            "second_team_id": row["second_team_id"],
        }
        for row in rows
    }
