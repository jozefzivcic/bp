#ifndef MYSQLNISTTESTSMANAGER_H
#define MYSQLNISTTESTSMANAGER_H
#include "inisttestsmanager.h"
#include "configstorage.h"
#include "ilogger.h"
#include <mysql_connection.h>
#include <cppconn/resultset.h>
#include <cppconn/prepared_statement.h>

class MySqlNistTestsManager : public INistTestsManager
{
private:
    sql::Driver *driver;
    sql::Connection* connection = nullptr;
    ILogger* logger = nullptr;
public:
    MySqlNistTestsManager(const ConfigStorage* storage);
    ~MySqlNistTestsManager();
    virtual bool getParameterById(long id, NistTestParameter& param) override;
private:
    void deleteStatementAndResSet(sql::PreparedStatement* p, sql::ResultSet* r);
};

#endif // MYSQLNISTTESTSMANAGER_H
