class PlayerView:
    @staticmethod
    def display_player(player):
        """display the details of a single player."""
        print(f"Name: {player.first_name} {player.last_name})")
        print(f"Date of birth: {player.birth_date}")
        print(f"Sex: {player.sex}")
        print(f"Chess ID: {player.chess_id}")
        print(f"Points: {player.pionts}")

    @staticmethod
    def display_players(players):
        """Display a list of players."""
        if not players:
            print("Players not found!")
        else:
            for player in players:
                print(f"{player.first_name} {player.last_name} (ID: {player.chess_id})")

@staticmethod
def get_player_details():
    """prompt the user to enter player information.
    """
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    birth_date = input("Enter birth date: ")
    sex = input("Enter sex (M/F): ")
    chess_id = input("Enter ID: ")
    return first_name, last_name, birth_date, sex, chess_id

