#ifndef MYSQLCURRENTLYRUNNINGMANAGER_H
#define MYSQLCURRENTLYRUNNINGMANAGER_H
#include "icurrentlyrunningmanager.h"
#include "mysql_connection.h"
#include "configstorage.h"
#include "ilogger.h"
#include "mysqldbpool.h"
#include <cppconn/driver.h>
#include <cppconn/resultset.h>
#include <cppconn/prepared_statement.h>

/**
 * @brief The MySqlCurrentlyRunningManager class implements interface ICurrentlyRunningManager.
 * For methods documentation see the interface.
 */
class MySqlCurrentlyRunningManager : public ICurrentlyRunningManager
{
private:
    ILogger* logger = nullptr;
    MySqlDBPool* dbPool = nullptr;
public:
    MySqlCurrentlyRunningManager(MySqlDBPool* pool);
    ~MySqlCurrentlyRunningManager();
    bool insertTest(Test t) override;
    bool removeTest(Test t) override;
};

#endif // MYSQLCURRENTLYRUNNINGMANAGER_H
