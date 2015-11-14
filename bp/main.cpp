//#include "mysql_connection.h"
//#include <cppconn/driver.h>
//#include <cppconn/exception.h>
//#include <cppconn/resultset.h>
//#include <cppconn/statement.h>

//using namespace std;

//int main(void)
//{
//try {
//  sql::Driver *driver;
//  sql::Connection *con;
//  sql::Statement *stmt;
//  sql::ResultSet *res;
//  /* Create a connection */
//  driver = get_driver_instance();
//  con = driver->connect("tcp://localhost:3306", "root", "admin");
//  /* Connect to the MySQL test database */
//  con->setSchema("mydb");

//  stmt = con->createStatement();
//  res = stmt->executeQuery("SELECT * FROM users");
//  while (res->next()) {
//    cout << res->getString("user_name") << endl;
//    cout << res->getString("user_password") << endl;
//  }
//  delete res;
//  delete stmt;
//  delete con;

//} catch (sql::SQLException &e) {
//  cout << "# ERR: SQLException in " << __FILE__;
//  //cout << "(" << __FUNCTION__ << ") on line " » << __LINE__ << endl;
//  cout << "# ERR: " << e.what();
//  cout << " (MySQL error code: " << e.getErrorCode();
//  cout << ", SQLState: " << e.getSQLState() << " )" << endl;
//}


//return EXIT_SUCCESS;
//}
#include <iostream>
#include "ifilemanager.h"
#include "mysqlfilemanager.h"
using namespace std;

int main(void) {
    IFileManager* fileManager = new MySqlFileManager();
    File f = fileManager->getFileById(1);
    cout << f.id() << " " << f.userId() << " " << f.hash() << " " << f.name() << " " << f.fileSystemPath() << endl;
    delete fileManager;
    return 0;
}
