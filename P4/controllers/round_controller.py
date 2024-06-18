from models.round import Round
from models.match import Match


class RoundController:
    def create_round(self, name):
        """
        Create a new round with the given name.
        :param name: The name of the round to create.
        :return:The new round.
        """
        round_ = Round(name)
        return round_

    def add_match_to_round(self, round_, player1, player2):
        """
        Add a match between two players to a specific round.

        :param round_: The round to which the match will be added.
        :param player1: The first player in the match.
        :param player2: The second player in the match.
        """
        match = Match(player1, player2)
        round_.add_match(match)

    def generate_results_for_round(self, round_):
        """
        Generate random results for all matches in a specific round.
        :param round_: The round for which the results will be generated.
        """
        round_.generate_results()