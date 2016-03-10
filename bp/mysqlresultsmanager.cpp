#include "mysqlresultsmanager.h"
#include <cppconn/driver.h>
#include <mutex>
#include "logger.h"

using namespace std;
using namespace sql;

extern mutex dbMutex;

MySqlResultsManager::MySqlResultsManager(MySqlDBPool *pool)
{
    logger = new Logger();
    dbPool = pool;
}

MySqlResultsManager::~MySqlResultsManager()
{
    if (logger != nullptr)
        delete logger;
}

bool MySqlResultsManager::storePathForTest(Test t, string path)
{
    Connection* connection = nullptr;
    PreparedStatement* preparedStmt = nullptr;
    try {
        connection = dbPool->getConnectionFromPoolBusy();
        preparedStmt = connection->prepareStatement("INSERT INTO results (id_test, directory) VALUES (?,?);");
        preparedStmt->setInt64(1,t.getId());
        preparedStmt->setString(2, path);
        preparedStmt->execute();
        if (preparedStmt != nullptr)
            delete preparedStmt;
        dbPool->releaseConnection(connection);
        return true;
    }catch(exception& ex) {
        logger->logError("storePathForTest " + string(ex.what()));
        if (preparedStmt != nullptr)
            delete preparedStmt;
        if (connection != nullptr)
            dbPool->releaseConnection(connection);
        return false;
    }
}

