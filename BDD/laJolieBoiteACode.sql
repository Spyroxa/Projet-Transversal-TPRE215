-- MySQL Script generated by MySQL Workbench
-- jeu. 31 mars 2022 11:40:16
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema laJolieBoiteACode
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema laJolieBoiteACode
DROP DATABASE IF EXISTS `laJolieBoiteACode`;
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `laJolieBoiteACode` DEFAULT CHARACTER SET utf8 ;
USE `laJolieBoiteACode` ;

-- -----------------------------------------------------
-- Table `laJolieBoiteACode`.`utilisateur`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `laJolieBoiteACode`.`utilisateur` (
  `id.utilisateur` INT NOT NULL AUTO_INCREMENT,
  `login` VARCHAR(45) NOT NULL,
  `motDePasse` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id.utilisateur`),
  UNIQUE INDEX `id.utilisateur_UNIQUE` (`id.utilisateur` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `laJolieBoiteACode`.`entreprise`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `laJolieBoiteACode`.`entreprise` (
  `identreprise` INT NOT NULL AUTO_INCREMENT,
  `nom` VARCHAR(45) NOT NULL,
  `n°siret` VARCHAR(45) NOT NULL,
  `adressePostale` VARCHAR(255) NOT NULL,
  `codePostal` VARCHAR(255) NOT NULL,
  `ville` VARCHAR(100) NOT NULL,
  `description` LONGTEXT NULL,
  `url` MEDIUMTEXT NULL,
  PRIMARY KEY (`identreprise`),
  UNIQUE INDEX `n°siret_UNIQUE` (`n°siret` ASC) ,
  UNIQUE INDEX `identreprise_UNIQUE` (`identreprise` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `laJolieBoiteACode`.`personne`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `laJolieBoiteACode`.`personne` (
  `idpersonne` INT NOT NULL AUTO_INCREMENT,
  `nom` VARCHAR(45) NOT NULL,
  `prenom` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `poste` VARCHAR(45) NULL,
  `telephone` VARCHAR(45) NULL,
  `statut` TINYINT NULL,
  `entreprise_identreprise` INT NOT NULL,
  PRIMARY KEY (`idpersonne`),
  UNIQUE INDEX `idpersonne_UNIQUE` (`idpersonne` ASC) ,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) ,
  INDEX `fk_personne_entreprise_idx` (`entreprise_identreprise` ASC) ,
  CONSTRAINT `fk_personne_entreprise`
    FOREIGN KEY (`entreprise_identreprise`)
    REFERENCES `laJolieBoiteACode`.`entreprise` (`identreprise`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `laJolieBoiteACode`.`facture`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `laJolieBoiteACode`.`facture` (
  `numeroFacture` INT NOT NULL,
  `dateEmission` DATE NOT NULL,
  `entreprise_identreprise` INT NOT NULL,
  `personne_idpersonne` INT NOT NULL,
  PRIMARY KEY (`numeroFacture`),
  INDEX `fk_facture_entreprise1_idx` (`entreprise_identreprise` ASC) ,
  INDEX `fk_facture_personne1_idx` (`personne_idpersonne` ASC) ,
  CONSTRAINT `fk_facture_entreprise1`
    FOREIGN KEY (`entreprise_identreprise`)
    REFERENCES `laJolieBoiteACode`.`entreprise` (`identreprise`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_facture_personne1`
    FOREIGN KEY (`personne_idpersonne`)
    REFERENCES `laJolieBoiteACode`.`personne` (`idpersonne`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `laJolieBoiteACode`.`commentaire`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `laJolieBoiteACode`.`commentaire` (
  `idcommentaire` INT NOT NULL AUTO_INCREMENT,
  `auteur` VARCHAR(45) NOT NULL,
  `description` VARCHAR(45) NULL,
  `dateDeCreation` DATE NOT NULL,
  `personne_idpersonne` INT NOT NULL,
  PRIMARY KEY (`idcommentaire`),
  UNIQUE INDEX `idcommentaire_UNIQUE` (`idcommentaire` ASC) ,
  INDEX `fk_commentaire_personne1_idx` (`personne_idpersonne` ASC) ,
  CONSTRAINT `fk_commentaire_personne1`
    FOREIGN KEY (`personne_idpersonne`)
    REFERENCES `laJolieBoiteACode`.`personne` (`idpersonne`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
