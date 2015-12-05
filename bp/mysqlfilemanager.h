#ifndef MYSQLFILEMANAGER
#define MYSQLFILEMANAGER
#include "ifilemanager.h"
#include "mysql_connection.h"
#include <cppconn/driver.h>
#include <cppconn/resultset.h>
#include <cppconn/prepared_statement.h>
class MySqlFileManager : public IFileManager {
private:
    sql::Connection* _con;
public:
    MySqlFileManager();
    bool getFileById(int id, File* file) override;
    ~MySqlFileManager();
private:
    void deleteStatementAndResSet(sql::PreparedStatement* p, sql::ResultSet* r);
};

#endif // MYSQLFILEMANAGER

