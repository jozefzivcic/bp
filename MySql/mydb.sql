SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

DROP DATABASE IF EXISTS mydb;
CREATE DATABASE mydb;
use mydb;

-- dropping tables
DROP TABLE IF EXISTS `currently_running`;
DROP TABLE IF EXISTS `files`;
DROP TABLE IF EXISTS `results`;
DROP TABLE IF EXISTS `tests`;
DROP TABLE IF EXISTS `users`;
DROP TABLE IF EXISTS `nist_tests`;
DROP TABLE IF EXISTS `change_table`;
DROP TRIGGER IF EXISTS `test_update`;
DROP TABLE IF EXISTS `groups`;
DROP TABLE IF EXISTS `groups_tests`;

-- creating tables
CREATE TABLE `users` (
  `id` int(11) PRIMARY KEY AUTO_INCREMENT,
  `user_name` varchar(64) NOT NULL,
  `user_password` varchar(64) NOT NULL
)DEFAULT CHARSET=utf8;

CREATE TABLE `files` (
  `id` int(11) PRIMARY KEY AUTO_INCREMENT,
  `id_user` int(11) NOT NULL,
  `hash` varchar(64) NOT NULL,
  `name` varchar(256) DEFAULT NULL,
  `file_system_path` varchar(1024),
  CONSTRAINT files_fk_id_user FOREIGN KEY (`id_user`) REFERENCES `users`(`id`)
)DEFAULT CHARSET=utf8;

CREATE TABLE `tests` (
  `id` int(11) PRIMARY KEY AUTO_INCREMENT,
  `id_file` int(11) NOT NULL,
  `id_user` int(11) NOT NULL,
  `time_of_add` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `test_table` varchar(16) NOT NULL, /*name of table with test parameters*/
  `loaded` tinyint(1) NOT NULL DEFAULT 0,  /*if test was loaded by external programm*/
  `num_of_runs` int(3) NOT NULL DEFAULT 0,
  `rerun` tinyint(1) DEFAULT 0,
  `time_of_rerun` timestamp DEFAULT CURRENT_TIMESTAMP,
  `loaded_for_rerun` tinyint(1) NOT NULL DEFAULT 0,
  `return_value` int(5) DEFAULT 0,
  `ended` tinyint(1) NOT NULL DEFAULT 0, /*if test ran and ended successfully*/
  CONSTRAINT tests_fk_id_user FOREIGN KEY (`id_user`) REFERENCES `users`(`id`),
  CONSTRAINT tests_fk_id_file FOREIGN KEY (`id_file`) REFERENCES `files`(`id`)
)DEFAULT CHARSET=utf8;

CREATE TABLE `currently_running` (
  `id_test` int(11) PRIMARY KEY,
  CONSTRAINT currently_running_fk_test_id FOREIGN KEY (`id_test`) REFERENCES `tests`(`id`)
)DEFAULT CHARSET=utf8;

CREATE TABLE `nist_tests` (
  `id_test` int(11) PRIMARY KEY,
  `length` int(11) NOT NULL,
  `test_number` int(5) NOT NULL,
  `streams` int(11),
  `special_parameter` int(11),
  CONSTRAINT nist_tests_fk_test_id FOREIGN KEY (`id_test`) REFERENCES `tests`(`id`)
)DEFAULT CHARSET=utf8;

CREATE TABLE `results` (
  `id_test` int(11) PRIMARY KEY,
  `directory` varchar(1024) NOT NULL,
  CONSTRAINT results_fk_test_id FOREIGN KEY (`id_test`) REFERENCES `tests`(`id`)
)DEFAULT CHARSET=utf8;

CREATE TABLE `groups` (
  `id` int(11) PRIMARY KEY AUTO_INCREMENT,
  `id_user` int(11),
  `time_of_add` timestamp DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT groups_fk_id_user FOREIGN KEY (`id_user`) REFERENCES `users`(`id`)
)DEFAULT CHARSET=utf8;

CREATE TABLE `groups_tests` (
  `id` int(11),
  `id_test` int(11),
  CONSTRAINT groups_tests_fk_test_id FOREIGN KEY (`id_test`) REFERENCES `tests`(`id`)
)DEFAULT CHARSET=utf8;

CREATE TABLE `change_table` (
  `id` INT(11) DEFAULT 0,
  `change_number` int(11) DEFAULT 0
)DEFAULT CHARSET=utf8;

INSERT INTO `change_table` (id,change_number) VALUES (0,0);

-- trigger for setting DB last state after insertion on tests
DELIMITER $$
CREATE TRIGGER `test_update` AFTER INSERT ON `tests` FOR EACH ROW
BEGIN
  DECLARE old_number INT;
  SELECT `change_number` INTO old_number FROM `change_table`;
  UPDATE `change_table` SET `change_number` = old_number + 1 WHERE `id` = 0;
END$$
DELIMITER ;

\. insertTestValues.sql
