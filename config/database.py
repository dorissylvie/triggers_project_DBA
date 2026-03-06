import mysql.connector
from mysql.connector import Error


DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "gestion_employes",
    "port": 3306,
}


def get_connection():
    """Retourne une connexion MySQL."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        raise ConnectionError(f"Erreur de connexion MySQL : {e}")


def test_connection():
    """Teste la connexion à la base de données."""
    try:
        conn = get_connection()
        conn.close()
        return True
    except ConnectionError:
        return False
