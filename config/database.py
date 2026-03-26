import mysql.connector
from mysql.connector import Error, pooling
import time

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "gestion_employes",
    "port": 3306,
}

# Pool de connexions
_connection_pool = None


def _init_pool():
    """Initialise le pool de connexions."""
    global _connection_pool
    if _connection_pool is None:
        try:
            _connection_pool = pooling.MySQLConnectionPool(
                pool_name="app_pool",
                pool_size=5,
                # Reset session on reuse to avoid stale transactions/snapshots.
                pool_reset_session=True,
                **DB_CONFIG,
            )
        except Error as e:
            raise ConnectionError(f"Erreur création pool MySQL : {e}")


def get_connection(retries=3, delay=1):
    """Retourne une connexion du pool avec retries."""
    global _connection_pool
    _init_pool()
    
    for attempt in range(retries):
        try:
            conn = _connection_pool.get_connection()
            # Keep each statement immediately visible across app instances.
            conn.autocommit = True
            return conn
        except Error as e:
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                raise ConnectionError(f"Erreur connexion MySQL après {retries} tentatives : {e}")


def test_connection():
    """Teste la connexion à la base de données."""
    try:
        conn = get_connection()
        conn.close()
        return True
    except ConnectionError:
        return False
