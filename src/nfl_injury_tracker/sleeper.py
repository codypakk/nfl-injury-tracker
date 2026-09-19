import time

import requests

sleeper_api = "https://api.sleeper.app/v1/players/nfl"

NFL_TEAMS = {
    "ARI",
    "ATL",
    "BAL",
    "BUF",
    "CAR",
    "CHI",
    "CIN",
    "CLE",
    "DAL",
    "DEN",
    "DET",
    "GB",
    "HOU",
    "IND",
    "JAX",
    "KC",
    "LAC",
    "LAR",
    "LV",
    "MIA",
    "MIN",
    "NE",
    "NO",
    "NYG",
    "NYJ",
    "PHI",
    "PIT",
    "SEA",
    "SF",
    "TB",
    "TEN",
    "WAS",
}

OFFENSIVE_POSITIONS = {"QB", "RB", "WR", "TE", "OL", "OT", "OG", "C", "T", "G", "FB"}


def fetch_injured_players(
    weeks: int = 4, only_starters: bool = False, only_offensive: bool = False
) -> dict[str, dict]:
    response = requests.get(sleeper_api)
    all_players = response.json()

    four_weeks_ms = weeks * 7 * 24 * 60 * 60 * 1000
    cutoff_time = (time.time() * 1000) - four_weeks_ms

    injured_players = {}

    for player_id, data in all_players.items():
        team = data.get("team")
        position = data.get("position")
        injury_status = data.get("injury_status")
        news_updated = data.get("news_updated")
        depth_order = data.get("depth_chart_order")

        if (
            team in NFL_TEAMS
            and injury_status
            and news_updated
            and news_updated >= cutoff_time
        ):
            if only_starters and depth_order != 1:
                continue
            if only_offensive and position not in OFFENSIVE_POSITIONS:
                continue

            injured_players[player_id] = {
                "player_id": player_id,
                "full_name": data.get("full_name"),
                "team": team,
                "position": position,
                "injury_status": injury_status,
                "news_updated": news_updated,
                "depth_chart_order": depth_order,
            }

    return injured_players
