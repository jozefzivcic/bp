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

-- creating tables
CREATE TABLE `users` (
  `id` int(11) PRIMARY KEY AUTO_INCREMENT,
  `user_name` varchar(45) NOT NULL,
  `user_password` varchar(45) NOT NULL
)DEFAULT CHARSET=utf8;

CREATE TABLE `files` (
  `id` int(11) PRIMARY KEY AUTO_INCREMENT,
  `id_user` int(11) NOT NULL,
  `hash` varchar(256) NOT NULL,
  `name` varchar(256) DEFAULT NULL,
  `file_system_path` varchar(1024),
  CONSTRAINT files_fk_id_user FOREIGN KEY (`id_user`) REFERENCES `users`(`id`)
)DEFAULT CHARSET=utf8;

CREATE TABLE `tests` (
  `id` int(11) PRIMARY KEY AUTO_INCREMENT,
  `id_file` int(11) NOT NULL,
  `id_user` int(11) NOT NULL,
  `time_of_add` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `test_table` varchar(45) NOT NULL, /*name of table with test parameters*/
  `run` tinyint(1) NOT NULL,  /*if test has already run*/
  `ended` tinyint(1) NOT NULL, /*if test ran and ended successfully*/
  CONSTRAINT tests_fk_id_user FOREIGN KEY (`id_user`) REFERENCES `users`(`id`),
  CONSTRAINT tests_fk_id_file FOREIGN KEY (`id_file`) REFERENCES `files`(`id`)
)DEFAULT CHARSET=utf8;

CREATE TABLE `currently_running` (
  `id_test` int(11) NOT NULL,
  CONSTRAINT currently_running_fk_test_id FOREIGN KEY (`id_test`) REFERENCES `tests`(`id`)
)DEFAULT CHARSET=utf8;

CREATE TABLE `nist_tests` (
  `id_test` int(11) NOT NULL,
  `parameter` int(11),
  CONSTRAINT nist_tests_fk_test_id FOREIGN KEY (`id_test`) REFERENCES `tests`(`id`)
)DEFAULT CHARSET=utf8;

CREATE TABLE `results` (
  `id_test` int(11) NOT NULL,
  `path1` varchar(1024) NOT NULL,
  `path2` varchar(1024) NOT NULL,
  CONSTRAINT results_fk_test_id FOREIGN KEY (`id_test`) REFERENCES `tests`(`id`)
)DEFAULT CHARSET=utf8;

\. insertTestValues.sql