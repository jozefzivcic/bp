INSERT INTO `users` (`user_name`, `user_password`) VALUES ('admin', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918');
INSERT INTO files (id_user, hash, name, file_system_path) VALUES (1,"AS654HASH","subor1","/home/jozef/Plocha/sts-2.1.2/data/data.sha1");
INSERT INTO files (id_user, hash, name, file_system_path) VALUES (1,"AS654HASH","subor1","/home/jozef/Plocha/sts-2.1.2/data/data.bad_rng");
INSERT INTO tests (id_file, id_user, test_table, loaded, ended) VALUES (1,1,"nist",0,0);
INSERT INTO tests (id_file, id_user, test_table, loaded, ended) VALUES (2,1,"nist",0,0);
INSERT INTO nist_tests (id_test, length, test_number, streams, special_parameter) VALUES(1,10000,15,1,400);
INSERT INTO nist_tests (id_test, length, test_number, streams, special_parameter) VALUES(2,10000,15,1,400);
