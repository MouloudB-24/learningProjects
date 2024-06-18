from pprint import pprint
from random import random, shuffle
from player import Player
from match import Match
from round import Round


class Tournament:
    def __init__(
        self,
        name=None,
        location=None,
        start_date=None,
        end_date=None,
        round_count=4,
        description="",
    ):
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.rounds_count = round_count
        self.description = description
        self.currend_round_number = 0
        self.rounds = []
        self.players = []
        self.match_history = {}

    def set_name(self, name):
        self.name = name

    def set_location(self, location):
        self.location

    def set_start_date(self, start_date):
        self.start_date = start_date

    def set_end_date(self, end_date):
        self.end_date = end_date

    def set_rounds_count(self, rounds_count):
        self.rounds_count = rounds_count

    def set_description(self, description):
        self.description = description

    def add_player(self, player):
        if isinstance(player, Player):
            self.players.append(player)
            if player.chess_id not in self.match_history:
                self.match_history[player.chess_id] = []

    def add_rounds(self, round_):
        if isinstance(round_, Round):
            self.rounds.append(round_)
            self.currend_round_number += 1

    def generate_pairs(self):
        # Sort players
        if self.currend_round_number == 1:
            random.shuffle(self.players)
        else:
            self.players.sort(key=lambda player: player.points, reverse=True)

        pairs = []
        used_players = set()

        # Manage the case where the number of players is odd
        bye_player = ""
        if len(self.players) % 2 != 0:
            for player in self.players:
                if player not in used_players:
                    bye_player = player
                    used_players.add(player)
                    break

        for i in range(len(self.players)):
            if self.players[i] in used_players:
                continue
            for j in range(i + 1, len(self.players)):
                if (
                    self.players[j] not in used_players
                    and self.players[j].chess_id
                    not in self.match_history[self.players[i].chess_id]
                ):

                    pairs.append((self.players[i], self.players[j]))
                    used_players.add(self.players[i])
                    used_players.add(self.players[j])
                    self.match_history[self.players[i].chess_id].append(self.players[j].chess_id)
                    self.match_history[self.players[j].chess_id].append(self.players[i].chess_id)
                    break

        if bye_player:
            print(f"{bye_player.chess_id} do no play in this round.")
        return pairs

    def generate_rounds(self):
        if self.currend_round_number > self.rounds_count:
            raise Exception("The maximun number of rounds has been reached")

        round_ = Round(name=f"Round {self.currend_round_number + 1}")
        pairs = self.generate_pairs()
        for player1, player2 in pairs:
            match = Match(player1, player2)
            round_.add_match(match)

        round_.generate_result()
        self.add_rounds(round_)
        return round_

    def to_dict(self):
        return {
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "currend_round_number": self.currend_round_number,
            "rounds_count": self.rounds_count,
            "description": self.description,
            "players": [player.chess_id for player in self.players],
            "rounds": [round_.to_dict() for round_ in self.rounds],
            "match_history": self.match_history,
        }

    @classmethod
    def from_dict(cls, data):
        tournament = cls(
            name=data["name"],
            location=data["location"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            rounds_number=data["rounds_count"],
            description=data["description"],
        )
        tournament.currend_round_number = data["currend_round_number"]
        tournament.players = [player_data for player_data in data["players"]]
        tournament.rounds = [
            Round.from_dict(round_data) for round_data in data["rounds"]
        ]
        tournament.match_history = data["match_history"]

        return tournament

    def __str__(self):
        return (
            f"Tournament: {self.name} at {self.location} from {self.start_date} to {self.end_date},"
            f"Rounds: {self.rounds}, Current round: {self.currend_round_number}, Players: {len(self.players)}"
            )


if __name__ == "__main__":
    tournament = Tournament("T", "Paris", "2024/06/09", "2024/08/09")
    aylan = Player("Aylan", "BELLIL", "2024/03/09", "M", "AB00001")
    mouloud = Player("Mouloud", "BELLIL", "1992/03/20", "M", "MB00002")
    tournament.add_player(aylan)
    tournament.add_player(mouloud)
    match1 = Match(aylan, mouloud)
    match2 = Match(mouloud, aylan)
    round1 = Round("Round1")
    round1.add_match(match1)
    round1.add_match(match2)
    tournament.generate_rounds()
    pprint(tournament.to_dict())
