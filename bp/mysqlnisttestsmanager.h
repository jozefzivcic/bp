#ifndef MYSQLNISTTESTSMANAGER_H
#define MYSQLNISTTESTSMANAGER_H
#include "inisttestsmanager.h"
#include "configstorage.h"
#include <mysql_connection.h>

class MySqlNistTestsManager : public INistTestsManager
{
private:
    sql::Connection* connection;
public:
    MySqlNistTestsManager(const ConfigStorage* storage);
    ~MySqlNistTestsManager();
    virtual bool getParameterById(long id, NistTestParameter& param) override;
};

#endif // MYSQLNISTTESTSMANAGER_H
