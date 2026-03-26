from utils.db_utils import execute_query, execute_non_query


class EmployeModel:
    """Opérations CRUD sur la table employe."""

    @staticmethod
    def get_all():
        return execute_query(
            "SELECT matricule, nom, salaire FROM employe ORDER BY matricule",
            fetch_all=True
        ) or []

    @staticmethod
    def get_by_matricule(matricule):
        return execute_query(
            "SELECT matricule, nom, salaire FROM employe WHERE matricule = %s",
            (matricule,),
            fetch_one=True
        )

    @staticmethod
    def insert(matricule, nom, salaire):
        execute_non_query(
            "INSERT INTO employe (matricule, nom, salaire) VALUES (%s, %s, %s)",
            (matricule, nom, salaire),
        )

    @staticmethod
    def update(matricule, nom, salaire):
        execute_non_query(
            "UPDATE employe SET nom = %s, salaire = %s WHERE matricule = %s",
            (nom, salaire, matricule),
        )

    @staticmethod
    def delete(matricule):
        execute_non_query(
            "DELETE FROM employe WHERE matricule = %s",
            (matricule,),
        )

    @staticmethod
    def search(keyword):
        like = f"%{keyword}%"
        return execute_query(
            "SELECT matricule, nom, salaire FROM employe WHERE matricule LIKE %s OR nom LIKE %s",
            (like, like),
            fetch_all=True
        ) or []
