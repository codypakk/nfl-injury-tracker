import json
import os

try:
    from sleeper import fetch_injured_players
except ImportError:
    from nfl_injury_tracker.sleeper import fetch_injured_players

STATE_FILE = "last_injured_players.json"


def load_previous_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {}


def save_current_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


def main():
    print("Fetching Sleeper API Data...")
    current_players = fetch_injured_players(
        weeks=4, only_starters=True, only_offensive=True
    )
    previous_players = load_previous_state()

    # Calculate differences
    current_ids = set(current_players.keys())
    previous_ids = set(previous_players.keys())

    added = [current_players[pid] for pid in current_ids - previous_ids]
    removed = [previous_players[pid] for pid in previous_ids - current_ids]

    print("\n--- Report ---")
    print(f"Total injured offensive starters: {len(current_players)}")

    if added:
        print("\nAdded to injury list:")
        for p in added:
            print(
                f" [+] {p['full_name']} ({p['position']} - {p['team']}): {p['injury_status']}"
            )

    if removed:
        print("\nRemoved from injury list:")
        for p in removed:
            print(f" [-] {p['full_name']} ({p['position']} - {p['team']})")

    # Save state for next run
    save_current_state(current_players)


if __name__ == "__main__":
    main()
