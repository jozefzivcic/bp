#ifndef MYSQLFILEMANAGER
#define MYSQLFILEMANAGER
#include "ifilemanager.h"
#include "configstorage.h"
#include <mysql_connection.h>
#include <cppconn/driver.h>
#include <cppconn/resultset.h>
#include <cppconn/prepared_statement.h>
class MySqlFileManager : public IFileManager {
private:
    sql::Connection* _con = nullptr;
public:
    MySqlFileManager(const ConfigStorage* storage);
    bool getFileById(int id, File* file) override;
    ~MySqlFileManager();
private:
    void deleteStatementAndResSet(sql::PreparedStatement* p, sql::ResultSet* r);
};

#endif // MYSQLFILEMANAGER

