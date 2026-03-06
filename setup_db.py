"""
Script d'initialisation de la base de données.
Exécute le schéma SQL et crée les triggers.

Usage : python setup_db.py
"""

import mysql.connector
from mysql.connector import Error


DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = ""
DB_PORT = 3306
DB_NAME = "gestion_employes"


def run_setup():
    try:
        conn = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, port=DB_PORT)
        cursor = conn.cursor()

        # Créer la base
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        cursor.execute(f"USE {DB_NAME}")
        print(f"[OK] Base de données '{DB_NAME}' prête.")

        # Table employe
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS employe (
                matricule VARCHAR(20) PRIMARY KEY,
                nom VARCHAR(100) NOT NULL,
                salaire DECIMAL(12, 2) NOT NULL
            )
        """)
        print("[OK] Table 'employe' créée.")

        # Table audit_employe
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_employe (
                id INT AUTO_INCREMENT PRIMARY KEY,
                type_action ENUM('AJOUT', 'MODIFICATION', 'SUPPRESSION') NOT NULL,
                date_mise_a_jour DATETIME DEFAULT CURRENT_TIMESTAMP,
                matricule VARCHAR(20) NOT NULL,
                nom VARCHAR(100),
                salaire_ancien DECIMAL(12, 2),
                salaire_nouv DECIMAL(12, 2),
                utilisateur VARCHAR(100) DEFAULT (CURRENT_USER())
            )
        """)
        print("[OK] Table 'audit_employe' créée.")

        # Triggers
        cursor.execute("DROP TRIGGER IF EXISTS trg_after_insert_employe")
        cursor.execute("""
            CREATE TRIGGER trg_after_insert_employe
            AFTER INSERT ON employe
            FOR EACH ROW
            INSERT INTO audit_employe (type_action, matricule, nom, salaire_ancien, salaire_nouv)
            VALUES ('AJOUT', NEW.matricule, NEW.nom, NULL, NEW.salaire)
        """)
        print("[OK] Trigger INSERT créé.")

        cursor.execute("DROP TRIGGER IF EXISTS trg_after_update_employe")
        cursor.execute("""
            CREATE TRIGGER trg_after_update_employe
            AFTER UPDATE ON employe
            FOR EACH ROW
            INSERT INTO audit_employe (type_action, matricule, nom, salaire_ancien, salaire_nouv)
            VALUES ('MODIFICATION', NEW.matricule, NEW.nom, OLD.salaire, NEW.salaire)
        """)
        print("[OK] Trigger UPDATE créé.")

        cursor.execute("DROP TRIGGER IF EXISTS trg_after_delete_employe")
        cursor.execute("""
            CREATE TRIGGER trg_after_delete_employe
            AFTER DELETE ON employe
            FOR EACH ROW
            INSERT INTO audit_employe (type_action, matricule, nom, salaire_ancien, salaire_nouv)
            VALUES ('SUPPRESSION', OLD.matricule, OLD.nom, OLD.salaire, NULL)
        """)
        print("[OK] Trigger DELETE créé.")

        conn.commit()
        cursor.close()
        conn.close()
        print("\n✅ Base de données initialisée avec succès !")
        print("   Vous pouvez maintenant lancer : python main.py")

    except Error as e:
        print(f"\n❌ Erreur MySQL : {e}")
        print("Vérifiez que MySQL est démarré et que les identifiants sont corrects.")


if __name__ == "__main__":
    run_setup()
