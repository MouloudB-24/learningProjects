class Player:
    def __init__(
        self, first_name=None, last_name=None, birth_date=None, sex="M", chess_id=None
    ):
        """_summary_

        Args:
            last_name (_type_, str): Nom de jouer. Defaults to None.
            first_name (_type_, str): prenom de joueur. Defaults to None.
            birth_date (_type_, date): date de naissance de joueur. Defaults to None.
            sex (_type_, str): sex de joueur. Defaults to M.
            chess_id (_type_, str): l'identifiant de joueur. Defaults to None.
        """
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.sex = sex
        self.chess_id = chess_id
        self.points = 0

    def set_first_name(self, first_name):
        self.first_name = first_name

    def set_last_name(self, last_name):
        self.last_name = last_name

    def set_birth_date(self, birth_date):
        self.birth_date = birth_date

    def set_sex(self, sex):
        self.sex = sex

    def set_chess_id(self, chess_id):
        self.chess_id = chess_id

    def add_points(self, points):
        """ajouter des points au joueur

        Args:
            points (_type_): le nombre de point à ajouter
        """
        self.points += points

    def to_dict(self):
        """Convertir les informations de joueur en dictionnaire pour le stockage en JSON.

        Returns:
            dict: Dictionnaire d'information de joueur
        """
        return {
            "last_name": self.last_name,
            "first_name": self.first_name,
            "birth_date": self.birth_date,
            "sex": self.sex,
            "chess_id": self.chess_id,
            "points": self.points,
        }

    @classmethod
    def from_dict(cls, data):
        """Créer un objet joueur depuis le dictionnaire de joueur (chargé depuis JSON).

        Args:
            data (dict): dictionnaire contenu les informations de joueur.

        Returns:
            object: objet joueur.
        """
        player = cls(
            first_name=data["first_name"],
            last_name=data["last_name",],
            birth_date=data["birth_date"],
            sex=data["sex"],
            chess_id=data["chess_id"],
        )
        player.points = data["points"]
        return player

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.chess_id})."


if __name__ == "__main__":
    aylan = Player("Aylan", "BELLIL", "2024/03/09", "M", "AB00001")
    print(aylan)
