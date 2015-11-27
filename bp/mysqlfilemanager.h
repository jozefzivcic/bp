#ifndef MYSQLFILEMANAGER
#define MYSQLFILEMANAGER
#include "ifilemanager.h"
#include "mysql_connection.h"
#include <cppconn/driver.h>
#include <cppconn/exception.h>
#include <cppconn/resultset.h>
#include <cppconn/prepared_statement.h>

class MySqlFileManager : public IFileManager {
private:
    sql::Connection* _con;
public:
    MySqlFileManager();
    bool getFileById(int id, File* file) const override;
    ~MySqlFileManager();
};

#endif // MYSQLFILEMANAGER

