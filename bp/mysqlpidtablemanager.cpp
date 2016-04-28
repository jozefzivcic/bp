#include "mysqlpidtablemanager.h"
#include "logger.h"
#include <cppconn/resultset.h>
#include <cppconn/prepared_statement.h>
using namespace std;
using namespace sql;

MySqlPIDTableManager::MySqlPIDTableManager(MySqlDBPool *pool)
{
    logger = new Logger();
    dbPool = pool;
}

MySqlPIDTableManager::~MySqlPIDTableManager()
{
    if (logger != nullptr)
        delete logger;
}

bool MySqlPIDTableManager::storePIDForId(int id, int pid)
{
    Connection* connection = nullptr;
    PreparedStatement* preparedStmt = nullptr;
    try {
        while((connection = dbPool->getConnectionFromPool()) == nullptr)
            std::this_thread::sleep_for(std::chrono::milliseconds(1));
        preparedStmt = connection->prepareStatement("INSERT INTO pid_table (id, pid) VALUES (?, ?);");
        preparedStmt->setInt(1, id);
        preparedStmt->setInt(2, pid);
        preparedStmt->execute();
        if (preparedStmt != nullptr)
            delete preparedStmt;
        dbPool->releaseConnection(connection);
        return true;
    }catch(exception& ex) {
        logger->logError("MySqlPIDTableManager::storePIDForId " + string(ex.what()));
        if (preparedStmt != nullptr)
            delete preparedStmt;
        if (connection != nullptr)
            dbPool->releaseConnection(connection);
        return false;
    }
}

bool MySqlPIDTableManager::removePIDForId(int id)
{
    Connection* connection = nullptr;
    PreparedStatement* preparedStmt = nullptr;
    try {
        while((connection = dbPool->getConnectionFromPool()) == nullptr)
            std::this_thread::sleep_for(std::chrono::milliseconds(1));
        preparedStmt = connection->prepareStatement("DELETE FROM pid_table WHERE id = ?;");
        preparedStmt->setInt(1, id);
        preparedStmt->execute();
        if (preparedStmt != nullptr)
            delete preparedStmt;
        dbPool->releaseConnection(connection);
        return true;
    }catch(exception& ex) {
        logger->logError("MySqlPIDTableManager::removePIDForId " + string(ex.what()));
        if (preparedStmt != nullptr)
            delete preparedStmt;
        if (connection != nullptr)
            dbPool->releaseConnection(connection);
        return false;
    }
}

