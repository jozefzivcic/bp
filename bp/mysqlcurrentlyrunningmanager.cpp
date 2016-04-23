#include "mysqlcurrentlyrunningmanager.h"
#include "mysql_connection.h"
#include "logger.h"
#include <cppconn/driver.h>
#include <cppconn/exception.h>
#include <cppconn/resultset.h>
#include <cppconn/prepared_statement.h>
#include <stdexcept>
#include <mutex>

using namespace std;
using namespace sql;

MySqlCurrentlyRunningManager::MySqlCurrentlyRunningManager(MySqlDBPool *pool)
{
    logger = new Logger();
    dbPool = pool;
}

MySqlCurrentlyRunningManager::~MySqlCurrentlyRunningManager()
{
    if (logger != nullptr)
        delete logger;
}

bool MySqlCurrentlyRunningManager::insertTest(Test t)
{
    Connection* connection = nullptr;
    PreparedStatement* preparedStmt = nullptr;
    try {
        while((connection = dbPool->getConnectionFromPool()) == nullptr)
            std::this_thread::sleep_for(std::chrono::milliseconds(1));
        preparedStmt = connection->prepareStatement("INSERT INTO currently_running (id_test) VALUES (?);");
        preparedStmt->setInt64(1,t.getId());
        preparedStmt->execute();
        if (preparedStmt != nullptr)
            delete preparedStmt;
        dbPool->releaseConnection(connection);
        return true;
    }catch(exception& ex) {
        logger->logError("insertTest " + string(ex.what()));
        if (preparedStmt != nullptr)
            delete preparedStmt;
        if (connection != nullptr)
            dbPool->releaseConnection(connection);
        return false;
    }
}

bool MySqlCurrentlyRunningManager::removeTest(Test t)
{
    Connection* connection = nullptr;
    PreparedStatement* preparedStmt = nullptr;
    try {
        while((connection = dbPool->getConnectionFromPool()) == nullptr)
            std::this_thread::sleep_for(std::chrono::milliseconds(1));
        preparedStmt = connection->prepareStatement("DELETE FROM currently_running WHERE id_test = ?;");
        preparedStmt->setInt64(1,t.getId());
        preparedStmt->execute();
        if (preparedStmt != nullptr)
            delete preparedStmt;
        dbPool->releaseConnection(connection);
        return true;
    }catch(exception& ex) {
        logger->logError("removeTest " + string(ex.what()));
        if (preparedStmt != nullptr)
            delete preparedStmt;
        if (connection != nullptr)
            dbPool->releaseConnection(connection);
        return false;
    }
}
