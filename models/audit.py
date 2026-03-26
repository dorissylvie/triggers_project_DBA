from utils.db_utils import execute_query


class AuditModel:
    """Requêtes sur la table audit_employe."""

    @staticmethod
    def get_all():
        return execute_query(
            "SELECT id, type_action, date_mise_a_jour, matricule, nom, "
            "salaire_ancien, salaire_nouv, utilisateur "
            "FROM audit_employe ORDER BY date_mise_a_jour DESC",
            fetch_all=True
        ) or []

    @staticmethod
    def get_stats():
        return execute_query(
            "SELECT "
            "SUM(CASE WHEN type_action = 'AJOUT' THEN 1 ELSE 0 END) AS nb_ajouts, "
            "SUM(CASE WHEN type_action = 'MODIFICATION' THEN 1 ELSE 0 END) AS nb_modifications, "
            "SUM(CASE WHEN type_action = 'SUPPRESSION' THEN 1 ELSE 0 END) AS nb_suppressions, "
            "COUNT(*) AS total "
            "FROM audit_employe",
            fetch_one=True
        )

    @staticmethod
    def filter_by_action(action_type):
        return execute_query(
            "SELECT id, type_action, date_mise_a_jour, matricule, nom, "
            "salaire_ancien, salaire_nouv, utilisateur "
            "FROM audit_employe WHERE type_action = %s "
            "ORDER BY date_mise_a_jour DESC",
            (action_type,),
            fetch_all=True
        ) or []
