#ifndef MYSQLCURRENTLYRUNNINGMANAGER_H
#define MYSQLCURRENTLYRUNNINGMANAGER_H
#include "icurrentlyrunningmanager.h"
#include "mysql_connection.h"
#include "configstorage.h"
#include <cppconn/driver.h>
#include <cppconn/resultset.h>
#include <cppconn/prepared_statement.h>

class MySqlCurrentlyRunningManager : public ICurrentlyRunningManager
{
private:
    sql::Driver *driver;
    sql::Connection* _con = nullptr;
public:
    MySqlCurrentlyRunningManager(const ConfigStorage* storage);
    ~MySqlCurrentlyRunningManager();
    bool insertTest(Test t) override;
    bool removeTest(Test t) override;
};

#endif // MYSQLCURRENTLYRUNNINGMANAGER_H
