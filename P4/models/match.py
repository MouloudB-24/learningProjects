import random
from player import Player


class Match:
    def __init__(self, player1, player2, score1=0, score2=0):
        self.player1 = player1
        self.score1 = score1
        self.player2 = player2
        self.score2 = score2

    def set_score(self, score1, score2):
        self.score1 = score1
        self.score2 = score2

    def generate_random_result(self):
        result = random.choice([(1, 0), (0, 1), (0.5, 0.5)])
        self.set_score(*result)
        self.update_points()

    def update_points(self):
        self.player1.points += self.score1
        self.player2.points += self.score2

    def to_dict(self):
        return {
            "player1": self.player1.chess_id,
            "score1": self.score1,
            "player2": self.player2.chess_id,
            "score2": self.score2,
        }

    @classmethod
    def form_to_dict(cls, data):
        player1 = Player.from_dict(data["player1"])
        player2 = Player.from_dict(data["player2"])
        return cls(player1, data["score1"], player2, data["score2"])

    def __str__(self):
        return f"{self.player1.chess_id} {self.score1} - {self.score2} {self.player2.chess_id}"


if __name__ == "__main__":
    aylan = Player("Aylan", "BELLIL", "2024/03/09", "M", "AB00001")
    mouloud = Player("Mouloud", "BELLIL", "1992/03/20", "M", "MB00002")
    match = Match(aylan, mouloud)
    match.generate_random_result()
    print(match)
    print(aylan.points)
    print(mouloud.points)
