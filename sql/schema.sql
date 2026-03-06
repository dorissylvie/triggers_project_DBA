-- =============================================
-- Base de données : gestion_employes
-- =============================================

CREATE DATABASE IF NOT EXISTS gestion_employes;
USE gestion_employes;

-- =============================================
-- Table : employe
-- =============================================

CREATE TABLE IF NOT EXISTS employe (
    matricule VARCHAR(20) PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    salaire DECIMAL(12, 2) NOT NULL
);

-- =============================================
-- Table : audit_employe
-- =============================================

CREATE TABLE IF NOT EXISTS audit_employe (
    id INT AUTO_INCREMENT PRIMARY KEY,
    type_action ENUM('AJOUT', 'MODIFICATION', 'SUPPRESSION') NOT NULL,
    date_mise_a_jour DATETIME DEFAULT CURRENT_TIMESTAMP,
    matricule VARCHAR(20) NOT NULL,
    nom VARCHAR(100),
    salaire_ancien DECIMAL(12, 2),
    salaire_nouv DECIMAL(12, 2),
    utilisateur VARCHAR(100) DEFAULT (CURRENT_USER())
);

-- =============================================
-- Trigger AFTER INSERT
-- =============================================

DROP TRIGGER IF EXISTS trg_after_insert_employe;

DELIMITER //
CREATE TRIGGER trg_after_insert_employe
AFTER INSERT ON employe
FOR EACH ROW
BEGIN
    INSERT INTO audit_employe (type_action, matricule, nom, salaire_ancien, salaire_nouv)
    VALUES ('AJOUT', NEW.matricule, NEW.nom, NULL, NEW.salaire);
END //
DELIMITER ;

-- =============================================
-- Trigger AFTER UPDATE
-- =============================================

DROP TRIGGER IF EXISTS trg_after_update_employe;

DELIMITER //
CREATE TRIGGER trg_after_update_employe
AFTER UPDATE ON employe
FOR EACH ROW
BEGIN
    INSERT INTO audit_employe (type_action, matricule, nom, salaire_ancien, salaire_nouv)
    VALUES ('MODIFICATION', NEW.matricule, NEW.nom, OLD.salaire, NEW.salaire);
END //
DELIMITER ;

-- =============================================
-- Trigger AFTER DELETE
-- =============================================

DROP TRIGGER IF EXISTS trg_after_delete_employe;

DELIMITER //
CREATE TRIGGER trg_after_delete_employe
AFTER DELETE ON employe
FOR EACH ROW
BEGIN
    INSERT INTO audit_employe (type_action, matricule, nom, salaire_ancien, salaire_nouv)
    VALUES ('SUPPRESSION', OLD.matricule, OLD.nom, OLD.salaire, NULL);
END //
DELIMITER ;
