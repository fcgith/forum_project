-- MariaDB Script
-- Updated to match the EER diagram
-- Generated for MariaDB compatibility

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8;
USE `mydb`;

-- -----------------------------------------------------
-- Table `users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`users`;

CREATE TABLE IF NOT EXISTS `mydb`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NOT NULL,
  `password` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `age` INT NOT NULL,
  `nickname` VARCHAR(45) NULL,
  `registration_date` DATE NOT NULL DEFAULT NOW(),
  `admin` TINYINT(1) NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC)
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `categories`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`categories`;

CREATE TABLE IF NOT EXISTS `mydb`.`categories` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `desc` VARCHAR(255) NOT NULL,
  `visibility` TINYINT(1) NULL DEFAULT 1,
  `locked` TINYINT(1) NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `topics`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`topics`;

CREATE TABLE IF NOT EXISTS `mydb`.`topics` (
  `id` VARCHAR(45) NOT NULL,
  `title` VARCHAR(45) NOT NULL,
  `desc` VARCHAR(255) NULL,
  `locked` TINYINT(1) NULL DEFAULT 0,
  `user_id` INT NOT NULL,
  `category_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_topics_users_idx` (`user_id` ASC),
  INDEX `fk_topics_categories_idx` (`category_id` ASC),
  CONSTRAINT `fk_topics_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `mydb`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_topics_categories`
    FOREIGN KEY (`category_id`)
    REFERENCES `mydb`.`categories` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `posts`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`posts`;

CREATE TABLE IF NOT EXISTS `mydb`.`posts` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(45) NOT NULL,
  `content` MEDIUMTEXT NOT NULL,
  `user_id` INT NOT NULL,
  `topic_id` VARCHAR(45) NOT NULL,
  `category_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_posts_users_idx` (`user_id` ASC),
  INDEX `fk_posts_topics_idx` (`topic_id` ASC),
  INDEX `fk_posts_categories_idx` (`category_id` ASC),
  CONSTRAINT `fk_posts_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `mydb`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_posts_topics`
    FOREIGN KEY (`topic_id`)
    REFERENCES `mydb`.`topics` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_posts_categories`
    FOREIGN KEY (`category_id`)
    REFERENCES `mydb`.`categories` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `replies`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`replies`;

CREATE TABLE IF NOT EXISTS `mydb`.`replies` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `post_id` INT NOT NULL,
  `reply_id` INT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_replies_posts_idx` (`post_id` ASC),
  INDEX `fk_replies_replies_idx` (`reply_id` ASC),
  CONSTRAINT `fk_replies_posts`
    FOREIGN KEY (`post_id`)
    REFERENCES `mydb`.`posts` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_replies_replies`
    FOREIGN KEY (`reply_id`)
    REFERENCES `mydb`.`replies` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `topic_interactions`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`topic_interactions`;

CREATE TABLE IF NOT EXISTS `mydb`.`topic_interactions` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `vote` TINYINT(1) NOT NULL DEFAULT 1,
  `topic_id` VARCHAR(45) NOT NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_topic_interactions_topics_idx` (`topic_id` ASC),
  INDEX `fk_topic_interactions_users_idx` (`user_id` ASC),
  CONSTRAINT `fk_topic_interactions_topics`
    FOREIGN KEY (`topic_id`)
    REFERENCES `mydb`.`topics` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_topic_interactions_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `mydb`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `post_interactions`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`post_interactions`;

CREATE TABLE IF NOT EXISTS `mydb`.`post_interactions` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `vote` TINYINT(1) NOT NULL DEFAULT 1,
  `post_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_post_interactions_posts_idx` (`post_id` ASC),
  INDEX `fk_post_interactions_users_idx` (`user_id` ASC),
  CONSTRAINT `fk_post_interactions_posts`
    FOREIGN KEY (`post_id`)
    REFERENCES `mydb`.`posts` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_post_interactions_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `mydb`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `replies_interactions`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`replies_interactions`;

CREATE TABLE IF NOT EXISTS `mydb`.`replies_interactions` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `vote` TINYINT(1) NOT NULL DEFAULT 1,
  `reply_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_replies_interactions_replies_idx` (`reply_id` ASC),
  INDEX `fk_replies_interactions_users_idx` (`user_id` ASC),
  CONSTRAINT `fk_replies_interactions_replies`
    FOREIGN KEY (`reply_id`)
    REFERENCES `mydb`.`replies` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_replies_interactions_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `mydb`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `conversations`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`conversations`;

CREATE TABLE IF NOT EXISTS `mydb`.`conversations` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `date` DATETIME NOT NULL,
  `initiator_id` INT NOT NULL,
  `receiver_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_conversations_initiator_idx` (`initiator_id` ASC),
  INDEX `fk_conversations_receiver_idx` (`receiver_id` ASC),
  CONSTRAINT `fk_conversations_initiator`
    FOREIGN KEY (`initiator_id`)
    REFERENCES `mydb`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_conversations_receiver`
    FOREIGN KEY (`receiver_id`)
    REFERENCES `mydb`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `direct_messages`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`direct_messages`;

CREATE TABLE IF NOT EXISTS `mydb`.`direct_messages` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `text` TEXT(255) NOT NULL,
  `date` DATETIME NOT NULL,
  `conversation_id` INT NOT NULL,
  `sender_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_direct_messages_conversations_idx` (`conversation_id` ASC),
  INDEX `fk_direct_messages_sender_idx` (`sender_id` ASC),
  CONSTRAINT `fk_direct_messages_conversations`
    FOREIGN KEY (`conversation_id`)
    REFERENCES `mydb`.`conversations` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_direct_messages_sender`
    FOREIGN KEY (`sender_id`)
    REFERENCES `mydb`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `category_access_privileges`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`category_access_privileges`;

CREATE TABLE IF NOT EXISTS `mydb`.`category_access_privileges` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `category_id` INT NOT NULL,
  `permission_type` TINYINT(1) NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  INDEX `fk_category_access_users_idx` (`user_id` ASC),
  INDEX `fk_category_access_categories_idx` (`category_id` ASC),
  CONSTRAINT `fk_category_access_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `mydb`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_category_access_categories`
    FOREIGN KEY (`category_id`)
    REFERENCES `mydb`.`categories` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;