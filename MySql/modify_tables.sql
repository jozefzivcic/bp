USE mydb;
ALTER TABLE groups ADD COLUMN total_tests BIGINT(11) DEFAULT NULL;
ALTER TABLE groups ADD COLUMN finished_tests BIGINT(11) NOT NULL DEFAULT 0;
ALTER TABLE groups ADD COLUMN stats TINYINT(1) NOT NULL DEFAULT 0;

CREATE TABLE `sid_cookies` (
  `sid_id` bigint(11) PRIMARY KEY AUTO_INCREMENT,
  `sid_str` varchar(64) NOT NULL,
  `user_id` bigint(11) NOT NULL,
  `time_of_add` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT sid_cookies_fk_user_id FOREIGN KEY (`user_id`) REFERENCES `users`(`id`)
)DEFAULT CHARSET=utf8;
