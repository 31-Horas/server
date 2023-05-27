-- MySQL Script generated by MySQL Workbench
-- Fri May 26 19:49:26 2023
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema otterboard
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema otterboard
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `otterboard` DEFAULT CHARACTER SET utf8 ;
USE `otterboard` ;

-- -----------------------------------------------------
-- Table `otterboard`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `otterboard`.`user` (
  `user_id` INT NOT NULL AUTO_INCREMENT,
  `user_email` VARCHAR(254) NOT NULL,
  `user_pswd` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`user_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `otterboard`.`bucketFile`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `otterboard`.`bucketFile` (
  `bucketFile_id` INT NOT NULL AUTO_INCREMENT,
  `bucketFile_name` VARCHAR(100) NOT NULL,
  `bucketFile_code` VARCHAR(45) NOT NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`bucketFile_id`, `user_id`),
  CONSTRAINT `fk_badgesFile_user`
    FOREIGN KEY (`user_id`)
    REFERENCES `otterboard`.`user` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE INDEX `fk_badgesFile_user_idx` ON `otterboard`.`bucketFile` (`user_id` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `otterboard`.`industryFile`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `otterboard`.`industryFile` (
  `industryFile_id` INT NOT NULL AUTO_INCREMENT,
  `industryFile_name` VARCHAR(45) NOT NULL,
  `industryFile_path` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`industryFile_id`))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;