INSERT INTO `users` (`user_name`, `user_password`) VALUES ('admin', 'admin');
INSERT INTO files (id_user, hash, name, file_system_path) VALUES (1,"AS654HASH","subor1","/home/jozef/Dokumenty/s1.txt");
INSERT INTO files (id_user, hash, name, file_system_path) VALUES (1,"AS654HASH","subor1","/home/jozef/Dokumenty/niečo s medzerou a ľščťžýáí.txt");
INSERT INTO tests (id_file, id_user, test_table, loaded, run, ended) VALUES (1,1,"nist",0,0,0);
INSERT INTO tests (id_file, id_user, test_table, loaded, run, ended) VALUES (2,1,"nist",0,0,0);
INSERT INTO tests (id_file, id_user, test_table, loaded, run, ended) VALUES (2,1,"nist",0,0,0);
SELECT id, id_file, id_user, UNIX_TIMESTAMP(time_of_add), test_table FROM tests WHERE run = 0 ORDER BY UNIX_TIMESTAMP(time_of_add);
