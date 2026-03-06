from config.database import get_connection


class EmployeModel:
    """Opérations CRUD sur la table employe."""

    @staticmethod
    def get_all():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT matricule, nom, salaire FROM employe ORDER BY matricule")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    @staticmethod
    def get_by_matricule(matricule):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT matricule, nom, salaire FROM employe WHERE matricule = %s", (matricule,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row

    @staticmethod
    def insert(matricule, nom, salaire):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO employe (matricule, nom, salaire) VALUES (%s, %s, %s)",
            (matricule, nom, salaire),
        )
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def update(matricule, nom, salaire):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE employe SET nom = %s, salaire = %s WHERE matricule = %s",
            (nom, salaire, matricule),
        )
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def delete(matricule):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM employe WHERE matricule = %s", (matricule,))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def search(keyword):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT matricule, nom, salaire FROM employe WHERE matricule LIKE %s OR nom LIKE %s"
        like = f"%{keyword}%"
        cursor.execute(query, (like, like))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
