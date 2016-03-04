#ifndef MYSQLRESULTSMANAGER_H
#define MYSQLRESULTSMANAGER_H
#include "iresultsmanager.h"
#include "ilogger.h"
#include "configstorage.h"
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
    sql::Driver *driver;
    sql::Connection* connection = nullptr;
    ILogger* logger = nullptr;
public:
    MySqlResultsManager(const ConfigStorage* storage);
    ~MySqlResultsManager();
    virtual bool storePathForTest(Test t, std::string path) override;
};

#endif // MYSQLRESULTSMANAGER_H
