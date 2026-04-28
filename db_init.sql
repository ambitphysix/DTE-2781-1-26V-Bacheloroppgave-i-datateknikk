-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema Soketeig
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema Soketeig
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `Soketeig` DEFAULT CHARACTER SET utf8mb4 ;
USE `Soketeig` ;

-- -----------------------------------------------------
-- Table `Soketeig`.`User`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Soketeig`.`User` (
  `UserID` INT(11) NOT NULL AUTO_INCREMENT,
  `UserName` VARCHAR(45) NOT NULL,
  `PasswordHash` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`UserID`),
  UNIQUE INDEX `username_UNIQUE` (`UserName` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `Soketeig`.`missing_categories`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Soketeig`.`missing_categories` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `kategori` VARCHAR(45) NOT NULL,
  `p25` DECIMAL(10,1) NOT NULL,
  `p50` DECIMAL(10,1) NOT NULL,
  `p75` DECIMAL(10,1) NOT NULL,
  `p95` DECIMAL(10,1) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 15
DEFAULT CHARACTER SET = utf8mb4;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;


USE `Soketeig`;

INSERT INTO `missing_categories` (`kategori`, `p25`, `p50`, `p75`, `p95`) VALUES
('Dement', 0.3, 0.8, 1.9, 8.3),
('Økt selvmordsrisiko', 0.3, 1.1, 3.2, 21.6),
('Psykisk utviklingshemmet', 0.6, 1.6, 3.2, 11.3),
('Autist', 0.6, 1.6, 3.7, 15.2),
('Rus', 0.5, 1.1, 4.2, 9.7),
('Barn 1-3', 0.2, 0.3, 0.6, 4.5),
('Barn 4-6', 0.2, 0.8, 1.5, 3.7),
('Barn 7-9', 0.8, 1.6, 3.2, 11.3),
('Barn 10-12', 0.8, 1.6, 3.2, 9.0),
('Barn 13-15', 0.8, 2.1, 4.8, 21.4),
('Turgåer', 1.1, 3.1, 5.8, 18.3),
('Jeger', 1.0, 2.1, 4.8, 17.2),
('Ski (alpin)', 1.1, 2.7, 4.8, 15.2),
('Ski (Langrenn)', 1.6, 3.5, 6.4, 19.6);
