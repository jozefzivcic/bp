SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

DROP DATABASE IF EXISTS mydb;
CREATE DATABASE mydb;
use mydb;

DROP TABLE IF EXISTS `currently_running`;
DROP TABLE IF EXISTS `files`;
DROP TABLE IF EXISTS `results`;
DROP TABLE IF EXISTS `tests`;
DROP TABLE IF EXISTS `users`;
DROP TABLE IF EXISTS `nist`;


CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(45) NOT NULL,
  `user_password` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
)DEFAULT CHARSET=utf8;

CREATE TABLE `files` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_user` int(11) NOT NULL,
  `hash` varchar(256) NOT NULL,
  `name` varchar(256) DEFAULT NULL,
  `file_system_path` varchar(1024) NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`id_user`) REFERENCES `users` (`id`)
)DEFAULT CHARSET=utf8;

CREATE TABLE `tests` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_file` int(11) NOT NULL,
  `id_user` int(11) NOT NULL,
  `time_of_add` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `test_parameter` int(11) NOT NULL,
  `run` tinyint(1) NOT NULL,
  `ended` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
)DEFAULT CHARSET=utf8;

CREATE TABLE `currently_running` (
  `id_test` int(11) NOT NULL
)DEFAULT CHARSET=utf8;

CREATE TABLE `nist_tests` (
  `id_test` int(11) NOT NULL,
  `parameter` int(11)
)DEFAULT CHARSET=utf8;

CREATE TABLE `results` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `path1` varchar(1024) NOT NULL,
  `path2` varchar(1024) NOT NULL,
  PRIMARY KEY (`id`)
)DEFAULT CHARSET=utf8;

INSERT INTO `users` (`id`, `user_name`, `user_password`) VALUES
(1, 'admin', 'admin');
insert into files (id, id_user, hash, name, file_system_path) VALUES (1,1,"AS654HASH","subor1","/home/jozef/Dokumenty/s1.txt");
