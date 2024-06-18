from controllers.player_controller import PlayerController
from controllers.tournament_controller import TournamentController
from views.view_player import PlayerView
from views.view_tournament import TournamentView
from views.view_round import RoundView


class MainController:
    def __init__(self):
        self.player_controller = PlayerController()
        self.tournament_controller = TournamentController()
        self.player_view = PlayerView()
        self.tournament_view = TournamentView()
        self.round_view = RoundView()

    def main_menu(self):
        while True:
            print("\n--- Main Menu ---")
            print("1. Manage Players")
            print("2. Manage Tournaments")
            print("3. Generate Reports")
            print("4. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.manage_players()
            elif choice == '2':
                self.manage_tournaments()
            elif choice == '3':
                self.generate_reports()
            elif choice == '4':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")

    def manage_players(self):
        while True:
            print("\n--- Manage Players ---")
            print("1. Add Player")
            print("2. List Players")
            print("3. Back to Main Menu")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.add_player()
            elif choice == '2':
                self.list_players()
            elif choice == '3':
                break
            else:
                print("Invalid choice. Please try again.")

    def add_player(self):
        try:
            #  Get player details
            last_name, first_name, birth_date, sex, chess_id = self.player_view.get_player_details()

            # Validate last name
            while not self.player_controller.is_valid_name(last_name):
                print("Invalid last name. It should not contain numbers or special characters.")
                last_name = input("Please enter a valid last name: ")

            # Validate first name
            while not self.player_controller.is_valid_name(first_name):
                print("Invalid first name. It should not contain numbers or special characters.")
                first_name = input("Please enter a valid first name: ")

            # Validate birthdate
            while not self.player_controller.is_valid_birth_date(birth_date):
                print("Invalid birth date format. It should be YYYY-MM-DD.")
                birth_date = input("Please enter a valid birth date (YYYY-MM-DD): ")

            # Validate sex
            while not self.player_controller.is_valid_sex(sex):
                print("Invalid sex. It should be 'M' or 'F'.")
                sex = input("Please enter a valid sex (M/F): ")

            # Validate chess ID
            while not self.player_controller.is_valid_chess_id(chess_id):
                print("Invalid chess ID format. It should be two letters followed by five digits.")
                chess_id = input("Please enter a valid chess ID: ")

            self.player_controller.add_player(last_name, first_name, birth_date, sex, chess_id)
            print("Player added successfully.")
        except Exception as e:
            print(f"Error adding player: {e}")

    def list_players(self):
        players = self.player_controller.list_players()
        if players:
            self.player_view.display_players(players)
        else:
            print("No players available.")

    def manage_tournaments(self):
        while True:
            print("\n--- Manage Tournaments ---")
            print("1. Create Tournament")
            print("2. List Tournaments")
            print("3. Add Player to Tournament")
            print("4. Display Tournament Details")
            print("5. Generate Round")
            print("6. Display Player Rankings")
            print("7. Back to Main Menu")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.create_tournament()
            elif choice == '2':
                self.list_tournaments()
            elif choice == '3':
                self.add_player_to_tournament()
            elif choice == '4':
                self.display_tournament_details()
            elif choice == '5':
                self.generate_round_for_tournament()
            elif choice == '6':
                self.display_player_rankings()
            elif choice == '7':
                break
            else:
                print("Invalid choice. Please try again.")

    def create_tournament(self):
        try:
            name, location, start_date, end_date, rounds_count, description = (
                self.tournament_view.get_tournament_details()
            )
            # Validate start date
            while not self.tournament_controller.is_valid_date(start_date):
                print("Invalid start date format. It should be YYYY-MM-DD.")
                start_date = input("Please enter a valid start date (YYYY-MM-DD): ")

            # Validate end date
            while not self.tournament_controller.is_valid_date(end_date):
                print("Invalid end date format. It should be YYYY-MM-DD.")
                end_date = input("Please enter a valid end date (YYYY-MM-DD): ")

            self.tournament_controller.create_tournament(name, location, start_date, end_date, rounds_count,
                                                         description)
            print("Tournament created successfully.")
        except Exception as e:
            print(f"Error creating tournament: {e}")

    def list_tournaments(self):
        tournaments = self.tournament_controller.list_tournaments()
        if tournaments:
            self.tournament_view.display_tournaments(tournaments)
        else:
            print("No tournaments available.")

    def add_player_to_tournament(self):
        try:
            tournament_name = self.tournament_view.get_tournament_name()
            chess_id = self.tournament_view.get_player_chess_id()
            player = self.player_controller.find_player_by_id(chess_id)
            if player:
                tournament = self.tournament_controller.find_tournament_by_name(tournament_name)
                if tournament:
                    if any(p.chess_id == chess_id for p in tournament.players):
                        print("Player is already added to the tournament.")
                    else:
                        success = self.tournament_controller.add_player_to_tournament(tournament_name, player)
                        if success:
                            print("Player added to tournament successfully.")
                        else:
                            print("Failed to add player to tournament.")
                else:
                    print("Tournament not found.")
            else:
                print("Player not found.")
        except Exception as e:
            print(f"Error adding player to tournament: {e}")

    def get_player_by_chess_id(self, chess_id, players_dict):
        return players_dict.get(chess_id)

    def display_tournament_details(self):
        try:
            tournament_name = self.tournament_view.get_tournament_name()
            tournament = self.tournament_controller.find_tournament_by_name(tournament_name)
            if tournament:
                self.tournament_view.display_tournament(tournament)
                for round_ in tournament.rounds:
                    self.round_view.display_round(round_)
            else:
                print("Tournament not found.")
        except Exception as e:
            print(f"Error displaying tournament details: {e}")

    def generate_round_for_tournament(self):
        try:
            tournament_name = self.tournament_view.get_tournament_name()
            round_ = self.tournament_controller.generate_round_for_tournament(tournament_name)
            if round_:
                try:
                    self.round_view.display_round(round_)
                    print("Round generated successfully.")

                except Exception as e:
                    print(f"Error generating round: {e}")
            else:
                print("Tournament not found.")
        except Exception as e:
            print(f"Error generating round: {e}")

    def display_player_rankings(self):
        try:
            tournament_name = self.tournament_view.get_tournament_name()
            tournament = self.tournament_controller.find_tournament_by_name(tournament_name)
            if tournament:
                rankings = self.tournament_controller.get_player_rankings(tournament)
                self.tournament_view.display_player_rankings(rankings)
            else:
                print("Tournament not found.")
        except Exception as e:
            print(f"Error displaying player rankings: {e}")

    def generate_reports(self):
        while True:
            print("\n--- Generate Reports ---")
            print("1. List all players (alphabetical order)")
            print("2. List all tournaments")
            print("3. Tournament details (name and dates)")
            print("4. List players in a tournament (alphabetical order)")
            print("5. List all rounds and matches in a tournament")
            print("6. Back to Main Menu")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.list_all_players()
            elif choice == '2':
                self.list_all_tournaments()
            elif choice == '3':
                self.tournament_details()
            elif choice == '4':
                self.list_players_in_tournament()
            elif choice == '5':
                self.list_rounds_and_matches()
            elif choice == '6':
                break
            else:
                print("Invalid choice. Please try again.")

    def list_all_players(self):
        players = self.player_controller.list_players()
        sorted_players = sorted(players, key=lambda player: (player.last_name, player.first_name))
        for player in sorted_players:
            print(player)

    def list_all_tournaments(self):
        tournaments = self.tournament_controller.list_tournaments()
        for tournament in tournaments:
            print(tournament)

    def tournament_details(self):
        tournament_name = self.tournament_view.get_tournament_name()
        tournament = self.tournament_controller.find_tournament_by_name(tournament_name)
        if tournament:
            print(f"Name: {tournament.name}")
            print(f"Location: {tournament.location}")
            print(f"Start Date: {tournament.start_date}")
            print(f"End Date: {tournament.end_date}")
        else:
            print("Tournament not found.")

    def list_players_in_tournament(self):
        tournament_name = self.tournament_view.get_tournament_name()
        tournament = self.tournament_controller.find_tournament_by_name(tournament_name)
        if tournament:
            sorted_players = sorted(tournament.players, key=lambda player: (player.last_name, player.first_name))
            for player in sorted_players:
                print(player)
        else:
            print("Tournament not found.")

    def list_rounds_and_matches(self):
        tournament_name = self.tournament_view.get_tournament_name()
        tournament = self.tournament_controller.find_tournament_by_name(tournament_name)
        if tournament:
            for round_ in tournament.rounds:
                print(f"{round_.name} - Start: {round_.start_time}, End: {round_.end_time}")
                for match in round_.matches:
                    print(
                        f"{match.player1.first_name} {match.player1.last_name} vs "
                        f"{match.player2.first_name} {match.player2.last_name} - "
                        f"Score: {match.score1}:{match.score2}"
                    )
        else:
            print("Tournament not found.")


if __name__ == "__main__":
    controller = MainController()
    controller.main_menu()