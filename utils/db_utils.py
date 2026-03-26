"""
Utilitaires pour les opérations DB sécurisées.
"""

from config.database import get_connection
from utils.session import get_current_username


def execute_query(query, params=None, fetch_one=False, fetch_all=False, commit=False):
    """
    Exécute une requête avec gestion garantie de fermeture.
    Définit automatiquement @app_user pour les triggers.
    
    :param query: Requête SQL
    :param params: Paramètres (tuple ou list)
    :param fetch_one: Récupérer un seul résultat
    :param fetch_all: Récupérer tous les résultats
    :param commit: Valider la transaction
    :return: Résultat (dict ou list)
    """
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Définir @app_user pour les triggers de manière sécurisée
        app_user = get_current_username() or "unknown"
        cursor.execute("SET @app_user = %s", (app_user,))
        
        cursor.execute(query, params or ())
        
        result = None
        if fetch_one:
            result = cursor.fetchone()
        elif fetch_all:
            result = cursor.fetchall()
        
        if commit:
            conn.commit()
        
        return result
    finally:
        if cursor:
            try:
                cursor.close()
            except:
                pass
        if conn:
            try:
                conn.close()
            except:
                pass


def execute_non_query(query, params=None):
    """
    Exécute une requête INSERT/UPDATE/DELETE avec commit automatique.
    
    :param query: Requête SQL
    :param params: Paramètres (tuple ou list)
    """
    execute_query(query, params, commit=True)
