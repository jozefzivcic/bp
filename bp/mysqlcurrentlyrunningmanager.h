#ifndef MYSQLCURRENTLYRUNNINGMANAGER_H
#define MYSQLCURRENTLYRUNNINGMANAGER_H
#include "icurrentlyrunningmanager.h"
#include "mysql_connection.h"
#include <cppconn/driver.h>
#include <cppconn/resultset.h>
#include <cppconn/prepared_statement.h>

class MySqlCurrentlyRunningManager : public ICurrentlyRunningManager
{
private:
    sql::Connection* _con;
public:
    MySqlCurrentlyRunningManager();
    ~MySqlCurrentlyRunningManager();
    bool insertTest(Test t) override;
    bool removeTest(Test t) override;
};

#endif // MYSQLCURRENTLYRUNNINGMANAGER_H
