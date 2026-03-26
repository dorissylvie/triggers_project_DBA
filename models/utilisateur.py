from utils.db_utils import execute_query


class UtilisateurModel:
    """Gestion de l'authentification utilisateur."""

    @staticmethod
    def authenticate(username, password):
        return execute_query(
            "SELECT nom, username, role "
            "FROM utilisateur "
            "WHERE username = %s AND mot_de_passe = SHA2(%s, 256)",
            (username, password),
            fetch_one=True
        )
