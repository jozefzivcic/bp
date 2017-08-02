ALTER TABLE tests ADD COLUMN group_id BIGINT(11) DEFAULT NULL;
ALTER TABLE tests ADD CONSTRAINT FOREIGN KEY tests_fk_group_id (`group_id`) REFERENCES `groups`(`id`);
