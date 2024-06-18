from datetime import datetime

from models.tournament import Tournament
from utils.data_manager import save_tournaments, load_tournaments


class TournamentController:
    def __init__(self):
        self.tournaments = load_tournaments()

    def create_tournament(self, name, location, start_date, end_date, rounds_count=4, description=""):
        """
        Create a new tournament and save it to the list of tournaments.
        :param name:The name of the tournament.
        :param location: The location where the tournament will be held.
        :param start_date: The start date of the tournament (format: YYYY-MM-DD)
        :param end_date: The end date of the tournament (format: YYYY-MM-DD).
        :param rounds_count: The number of rounds in the tournament (default is 4).
        :param description: A brief description of the tournament.
        """
        tournament = Tournament(name, location, start_date, end_date, rounds_count, description)
        self.tournaments.append(tournament)
        save_tournaments(self.tournaments)

    def list_tournaments(self):
        """
        Retrieve the list of all tournaments.
        :return: list of Tournament objects representing all the tournaments.
        """
        return self.tournaments

    def find_tournament_by_name(self, name):
        """
        Find a tournament by its name.
        :param name: The name of the tournament to find.
        :return: Tournament object if found, None otherwise.
        """
        for tournament in self.tournaments:
            if tournament.name == name:
                return tournament
        return None

    def add_player_to_tournament(self, tournament_name, player):
        """
        Add a player to a specific tournament by its name.
        :param tournament_name: The name of the tournament to which the player will be added.
        :param player: The player to add to the tournament.
        :return: True if the player was successfully added, False if the tournament was not found.
        """
        tournament = self.find_tournament_by_name(tournament_name)
        if tournament:
            tournament.add_player(player)
            save_tournaments(self.tournaments)
            return True
        return False

    def add_round_to_tournament(self, tournament_name, round_):
        """
        Add a round to a specific tournament by its name.
        :param tournament_name: The name of the tournament to which the round will be added.
        :param round_: The round to add to the tournament.
        :return: True if the round was successfully added, False if the tournament was not found.
        """
        tournament = self.find_tournament_by_name(tournament_name)
        if tournament:
            tournament.add_round(round_)
            save_tournaments(self.tournaments)
            return True
        return False

    def generate_pairs_for_tournament(self, tournament_name):
        """
        Generate pairs of players for the next round of a specific tournament by its name.
        :param tournament_name: The name of the tournament for which pairs will be generated.
        :return: list of tuples: A list of player pairs (tuples) if the tournament is found,
        None otherwise.
        """
        tournament = self.find_tournament_by_name(tournament_name)
        if tournament:
            pairs = tournament.generate_pairs()
            save_tournaments(self.tournaments)
            return pairs
        return None

    def get_player_rankings(self, tournament):
        """
         Get the player rankings for a specific tournament.
        :param tournament: The tournament for which to get the player rankings.
        :return: list of Player objects: A list of players sorted by their points in descending order.
        """
        players = tournament.players
        players.sort(key=lambda player: player.points, reverse=True)
        return players

    def generate_round_for_tournament(self, tournament_name):
        """
        Generate the next round for a specific tournament by its name.
        :param tournament_name: The name of the tournament for which to generate the next round.
        :return: Round object if the round was successfully generated, None if the tournament was
        not found.
        """
        tournament = self.find_tournament_by_name(tournament_name)
        if tournament:
            round_ = tournament.generate_round()
            save_tournaments(self.tournaments)
            return round_
        return None

    def is_valid_date(self, date_str):
        """
        Validate if a given string is a valid date in the format YYYY-MM-DD.
        :param date_str: The date string to validate.
        :return: True if the date string is valid, False otherwise.
        """
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False