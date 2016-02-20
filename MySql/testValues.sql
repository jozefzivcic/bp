START TRANSACTION;
INSERT INTO tests (id_file, id_user, test_table, loaded, ended) VALUES (1,1,"nist",0,0);
INSERT INTO tests (id_file, id_user, test_table, loaded, ended) VALUES (2,1,"nist",0,0);
INSERT INTO nist_tests (id_test, length, test_number, streams, special_parameter) VALUES(3,10000,1,1,NULL);
INSERT INTO nist_tests (id_test, length, test_number, streams, special_parameter) VALUES(4,10000,3,1, NULL);
COMMIT;
