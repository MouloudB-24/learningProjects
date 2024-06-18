import re
from datetime import datetime

from models.player import Player
from utils.data_manager import save_players, load_players


class PlayerController:
    def __init__(self):
        self.players = load_players()

    def add_player(self, last_name, first_name, birth_date, sex, chess_id):
        if not self.is_valid_name(last_name):
            raise ValueError("Invalid last name. It should not contain numbers or special characters.")
        if not self.is_valid_name(first_name):
            raise ValueError("Invalid first name. It should not contain numbers or special characters.")
        if not self.is_valid_chess_id(chess_id):
            raise ValueError("Invalid chess ID format. It should be two letters followed by five digits.")
        if not self.is_valid_sex(sex):
            raise ValueError("Invalid sex. It should be 'M' or 'F'.")
        if not self.is_valid_birth_date(birth_date):
            raise ValueError("Invalid birth date format. It should be YYYY-MM-DD.")
        if self.player_exists(chess_id):
            raise ValueError(f"A player with chess ID {chess_id} already exists.")

        player = Player(last_name, first_name, birth_date, sex, chess_id)
        self.players.append(player)
        save_players(self.players)

    def player_exists(self, chess_id):
        """
        Check if a player with the given chess_id already exists.
        :param chess_id: The chess ID to check
        :return: True if a player with the chess_id exists, False otherwise
        """
        return any(player.chess_id == chess_id for player in self.players)

    def list_players(self):
        return self.players

    def find_player_by_id(self, chess_id):
        for player in self.players:
            if player.chess_id == chess_id:
                return player
        return None

    def is_valid_name(self, name):
        """
        Validate that the name does not contain numbers or special characters.
        :param name: The name to validate
        :return: True if the name is valid, False otherwise
        """
        pattern = re.compile(r'^[A-Za-zÀ-ÖØ-öø-ÿ]+$')
        return bool(pattern.match(name))

    def is_valid_birth_date(self, birth_date):
        """
        Validate that the birth date is in the format YYYY-MM-DD.
        :param birth_date: The birth date to validate
        :return: True if the birth date is valid, False otherwise
        """
        try:
            datetime.strptime(birth_date, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def is_valid_chess_id(self, chess_id):
        """
        Validate the chess ID format: two letters followed by five digits.
        :param chess_id: The chess ID to validate
        :return: True if the format is correct, False otherwise
        """
        pattern = re.compile(r'^[A-Za-z]{2}\d{5}$')
        return bool(pattern.match(chess_id))

    def is_valid_sex(self, sex):
        """
        Validate that the sex is either 'M' or 'F'.
        :param sex: The sex to validate
        :return: True if the sex is valid, False otherwise
        """
        return sex in ['M', 'F']