import json
from models.player import Player
from models.tournament import Tournament
from config import save_folder


def load_players():
    try:
        with open(save_folder / "players.json", 'r', encoding='utf-8') as file:
            players_data = json.load(file)
            return [Player.from_dict(player) for player in players_data]
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Error decoding JSON from players.json")
        return []


def save_players(players):
    try:
        with open(save_folder / "players.json", 'w', encoding='utf-8') as file:
            json.dump([player.to_dict() for player in players], file, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving players: {e}")


def load_tournaments():
    try:
        with open(save_folder / 'tournaments.json', 'r', encoding='utf-8') as file:
            tournaments_data = json.load(file)
            return [Tournament.from_dict(tournament) for tournament in tournaments_data]
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Error decoding JSON from tournaments.json")
        return []


def save_tournaments(tournaments):
    try:
        with open(save_folder / 'tournaments.json', 'w', encoding='utf-8') as file:
            json.dump([tournament.to_dict() for tournament in tournaments], file, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving tournaments: {e}")