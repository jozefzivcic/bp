#ifndef MYSQLNISTTESTSMANAGER_H
#define MYSQLNISTTESTSMANAGER_H
#include "inisttestsmanager.h"
#include "configstorage.h"
#include <mysql_connection.h>
#include <cppconn/resultset.h>
#include <cppconn/prepared_statement.h>

class MySqlNistTestsManager : public INistTestsManager
{
private:
    sql::Connection* connection = nullptr;
public:
    MySqlNistTestsManager(const ConfigStorage* storage);
    ~MySqlNistTestsManager();
    virtual bool getParameterById(long id, NistTestParameter& param) override;
private:
    void deleteStatementAndResSet(sql::PreparedStatement* p, sql::ResultSet* r);
};

#endif // MYSQLNISTTESTSMANAGER_H
