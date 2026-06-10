import random

GROUP_IDS = [chr(ord("A") + i) for i in range(12)]

# Sorteio único e global dos grupos cujo 3º colocado avança (mesmo para todos os participantes).
THIRD_PLACE_GROUPS = random.Random(2026).sample(GROUP_IDS, 8)

# Estrutura fixa da Rodada de 32 (formato simplificado, baseado no padrão da FIFA).
ROUND_OF_32_TEMPLATE = [
    ("1A", "2B"), ("1C", "2D"), ("1E", "2F"), ("1G", "2H"),
    ("1I", "2J"), ("1K", "2L"),
    ("1B", "3-1"), ("1D", "3-2"), ("1F", "3-3"), ("1H", "3-4"), ("1J", "3-5"), ("1L", "3-6"),
    ("2A", "2C"), ("2E", "2G"), ("2I", "2K"),
    ("3-7", "3-8"),
]

STAGE_NAMES = ["Rodada de 32", "Oitavas de Final", "Quartas de Final", "Semifinal", "Final"]


def _third_place_team(group_teams, first_id, second_id):
    remaining = [t for t in group_teams if t["id"] not in (first_id, second_id)]
    remaining.sort(key=lambda t: t["position"])
    return remaining[0]


def build_round_of_32(groups, picks):
    """Monta a Rodada de 32 com base nos palpites de 1º/2º de cada grupo."""
    teams_by_group = {g["id"]: g["teams"] for g in groups}

    slots = {}
    for group_id, group_teams in teams_by_group.items():
        pick = picks[group_id]
        first_team = next(t for t in group_teams if t["id"] == pick["first_team_id"])
        second_team = next(t for t in group_teams if t["id"] == pick["second_team_id"])
        slots[f"1{group_id}"] = first_team
        slots[f"2{group_id}"] = second_team

    for i, group_id in enumerate(THIRD_PLACE_GROUPS, start=1):
        pick = picks[group_id]
        slots[f"3-{i}"] = _third_place_team(
            teams_by_group[group_id], pick["first_team_id"], pick["second_team_id"]
        )

    return [(slots[a], slots[b]) for a, b in ROUND_OF_32_TEMPLATE]


def simulate_bracket(participant_id, round_of_32):
    """Sorteia (de forma determinística por participante) os vencedores até o campeão.

    Retorna (rounds, winners_per_round, champion):
    - rounds[i]: lista de confrontos (par de times) da fase i
    - winners_per_round[i]: vencedores correspondentes a rounds[i]
    """
    rng = random.Random(participant_id)
    rounds = [round_of_32]
    winners_per_round = []
    current = round_of_32

    while True:
        winners = [rng.choice(match) for match in current]
        winners_per_round.append(winners)
        if len(winners) == 1:
            break
        current = [(winners[i], winners[i + 1]) for i in range(0, len(winners), 2)]
        rounds.append(current)

    champion = winners_per_round[-1][0]
    return rounds, winners_per_round, champion
