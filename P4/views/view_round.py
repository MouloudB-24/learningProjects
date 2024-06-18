class RoundView:
    @staticmethod
    def display_round(round_):
        """Display the details of a single round."""
        print(f"Round Name: {round_.name}")
        print(f"Start Time: {round_.start_time}")
        print("End Time: {round_.end_time}")
        print("/nMatches:")
        for match in round_.martchs:
            print(
                f"{match.player1.first_name} {match.player1.last_name} {match.score1} - {match.score2} {match.player2.first_name} {match.player2.last_name}"
            )

    @staticmethod
    def display_rounds(rounds):
        """Displays a list of rounds."""
        if not rounds:
            print("No rounds avialable.")
        else:
            for round_ in rounds:
                print(
                    f"{round_.name} Start: {round_start_time} - End: {round_end_time}"
                )
