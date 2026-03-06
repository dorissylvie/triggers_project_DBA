from config.database import get_connection


class AuditModel:
    """Requêtes sur la table audit_employe."""

    @staticmethod
    def get_all():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, type_action, date_mise_a_jour, matricule, nom, "
            "salaire_ancien, salaire_nouv, utilisateur "
            "FROM audit_employe ORDER BY date_mise_a_jour DESC"
        )
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    @staticmethod
    def get_stats():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT "
            "SUM(CASE WHEN type_action = 'AJOUT' THEN 1 ELSE 0 END) AS nb_ajouts, "
            "SUM(CASE WHEN type_action = 'MODIFICATION' THEN 1 ELSE 0 END) AS nb_modifications, "
            "SUM(CASE WHEN type_action = 'SUPPRESSION' THEN 1 ELSE 0 END) AS nb_suppressions, "
            "COUNT(*) AS total "
            "FROM audit_employe"
        )
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row

    @staticmethod
    def filter_by_action(action_type):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, type_action, date_mise_a_jour, matricule, nom, "
            "salaire_ancien, salaire_nouv, utilisateur "
            "FROM audit_employe WHERE type_action = %s "
            "ORDER BY date_mise_a_jour DESC",
            (action_type,),
        )
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
