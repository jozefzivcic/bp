USE mydb;
ALTER TABLE groups ADD COLUMN total_tests BIGINT(11) DEFAULT NULL;
ALTER TABLE groups ADD COLUMN finished_tests BIGINT(11) NOT NULL DEFAULT 0;
ALTER TABLE groups ADD COLUMN stats TINYINT(1) NOT NULL DEFAULT 0;
