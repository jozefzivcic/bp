#ifndef MYSQLRESULTSMANAGER_H
#define MYSQLRESULTSMANAGER_H
#include "iresultsmanager.h"
#include "ilogger.h"
#include "configstorage.h"
#include "mysqldbpool.h"
#include <mysql_connection.h>
#include <cppconn/resultset.h>
#include <cppconn/prepared_statement.h>

/**
 * @brief The MySqlResultsManager class implements interface IResultsManager. For methods description
 * see interface.
 */
class MySqlResultsManager : public IResultsManager
{
private:
    ILogger* logger = nullptr;
    MySqlDBPool* dbPool = nullptr;
public:
    MySqlResultsManager(MySqlDBPool* pool);
    ~MySqlResultsManager();
    virtual bool storePathForTest(Test t, std::string path) override;
};

#endif // MYSQLRESULTSMANAGER_H
