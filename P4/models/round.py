from datetime import datetime
from match import Match


class Round:
    def __init__(self, name=None, start_time=None, end_time=None):
        self.name = name
        self.start_time = (
            start_time if start_time else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        self.end_time = end_time
        self.matchs = []

    def set_name(self, name):
        self.name = name

    def set_start_time(self, start_time):
        self.start_time = start_time

    def set_end_time(self, end_time):
        self.end_time = end_time

    def add_match(self, match):
        if isinstance(match, Match):
            self.matchs.append(match)

    def generate_result(self):
        for match in self.matchs:
            match.generate_random_result()
        self.end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "name": self.name,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "matchs": [match.to_dict() for match in self.matchs],
        }

    @classmethod
    def from_dict(cls, data):
        round_ = cls(
            name=data["name"], start_time=data["start_time"], end_time=data["end_time"]
        )
        round_.matchs = [
            Match.form_to_dict(match_data) for match_data in data["matchs"]
        ]
        return round_

    def __str__(self):
        return f"Name : {self.name} Start : {self.start_time} End : {self.end_time} Matchs : {len(self.matchs)}"


if __name__ == "__main__":
    from player import Player

    aylan = Player("Aylan", "BELLIL", "2024/03/09", "M", "AB00001")
    mouloud = Player("Mouloud", "BELLIL", "1992/03/20", "M", "MB00002")
    match1 = Match(aylan, mouloud)
    match2 = Match(mouloud, aylan)
    round1 = Round("Round1")
    round1.add_match(match1)
    round1.add_match(match2)
    round1.generate_result()
    print(match1)
    print(match2)
    print(round1)
