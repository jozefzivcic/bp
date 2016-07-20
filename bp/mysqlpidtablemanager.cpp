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

bool MySqlPIDTableManager::storePIDForId(long id, int pid)
{
    Connection* connection = nullptr;
    PreparedStatement* preparedStmt = nullptr;
    try {
        while((connection = dbPool->getConnectionFromPool()) == nullptr)
            std::this_thread::sleep_for(std::chrono::milliseconds(1));
        preparedStmt = connection->prepareStatement("INSERT INTO pid_table (id, pid) VALUES (?, ?);");
        preparedStmt->setInt64(1, id);
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

bool MySqlPIDTableManager::removePIDForId(long id)
{
    Connection* connection = nullptr;
    PreparedStatement* preparedStmt = nullptr;
    try {
        while((connection = dbPool->getConnectionFromPool()) == nullptr)
            std::this_thread::sleep_for(std::chrono::milliseconds(1));
        preparedStmt = connection->prepareStatement("DELETE FROM pid_table WHERE id = ?;");
        preparedStmt->setInt64(1, id);
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

bool MySqlPIDTableManager::getPIDForId(long id, pid_t &pid)
{
    Connection* connection = nullptr;
    PreparedStatement* preparedStmt = nullptr;
    ResultSet *res = nullptr;
    pid_t tempPID = 0;
    try {
        while((connection = dbPool->getConnectionFromPool()) == nullptr)
            std::this_thread::sleep_for(std::chrono::milliseconds(1));
        preparedStmt = connection->prepareStatement("SELECT pid FROM pid_table WHERE id = ?;");
        preparedStmt->setInt64(1,id);
        res = preparedStmt->executeQuery();
        int i = 0;
        while (res->next()) {
            tempPID = res->getInt("pid");
            i++;
        }
        if (i == 1)
            pid = tempPID;
        freeResources(connection, preparedStmt,res);
        return i == 1;
    }catch(exception& ex) {
        logger->logError("MySqlPIDTableManager::getPIDForId " + string(ex.what()));
        freeResources(connection, preparedStmt,res);
        return false;
    }
}

void MySqlPIDTableManager::freeResources(Connection* con, PreparedStatement* p, ResultSet* r)
{
    if (p != nullptr)
        delete p;
    if (r != nullptr)
        delete r;
    if (con != nullptr)
        dbPool->releaseConnection(con);
}
