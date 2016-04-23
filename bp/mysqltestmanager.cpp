#include "mysqltestmanager.h"
#include "logger.h"
#include <cppconn/driver.h>
#include <mutex>

using namespace std;
using namespace sql;

MySqlTestManager::MySqlTestManager(MySqlDBPool *pool)
{
    logger = new Logger();
    dbPool = pool;
}
MySqlTestManager::~MySqlTestManager()
{
    if (logger != nullptr)
        delete logger;
}

bool MySqlTestManager::getAllTestsReadyForRunning(list<Test>& t)
{
    Connection* connection = nullptr;
    PreparedStatement* preparedStmt = nullptr;
    ResultSet* res = nullptr;
    list<Test> l;
    try{
        while((connection = dbPool->getConnectionFromPool()) == nullptr)
            std::this_thread::sleep_for(std::chrono::milliseconds(1));
        preparedStmt = connection->prepareStatement("SELECT id, id_file, id_user, UNIX_TIMESTAMP(time_of_add) time, test_table, num_of_runs, rerun, UNIX_TIMESTAMP(time_of_rerun) time_rr, return_value FROM tests WHERE (loaded = 0) OR (rerun = 1 AND time_of_rerun <= CURRENT_TIMESTAMP);");
        res = preparedStmt->executeQuery();
        while(res->next()) {
            Test t;
            t.setId(res->getInt64("id"));
            t.setFileId(res->getInt64("id_file"));
            t.setUserId(res->getInt64("id_user"));
            t.setTimeOfAdd(res->getInt("time"));
            t.setTestTable(res->getString("test_table"));
            t.setNumOfRuns(res->getInt("num_of_runs"));
            t.setRerun(res->getBoolean("rerun"));
            t.setTimeOfRerun(res->getInt("time_rr"));
            t.setReturnValue(res->getInt("return_value"));
            l.push_back(t);
        }
        freeResources(connection, preparedStmt, res);
        t.insert(t.end(), l.begin(), l.end());
        return true;
    }catch(exception& ex) {
        logger->logError("getAllTestsReadyForRunning " + string(ex.what()));
        freeResources(connection, preparedStmt, res);
        return false;
    }
}

bool MySqlTestManager::getTestsNotFinished(std::list<Test> &t)
{
    Connection* connection = nullptr;
    PreparedStatement* preparedStmt = nullptr;
    ResultSet* res = nullptr;
    list<Test> l;
    try{
        while((connection = dbPool->getConnectionFromPool()) == nullptr)
            std::this_thread::sleep_for(std::chrono::milliseconds(1));
        preparedStmt = connection->prepareStatement("SELECT id, id_file, id_user, UNIX_TIMESTAMP(time_of_add) time, test_table, num_of_runs, rerun, UNIX_TIMESTAMP(time_of_rerun) time_rr, return_value FROM tests WHERE loaded = 1 AND ended = 0;");
        res = preparedStmt->executeQuery();
        while(res->next()) {
            Test t;
            t.setId(res->getInt64("id"));
            t.setFileId(res->getInt64("id_file"));
            t.setUserId(res->getInt64("id_user"));
            t.setTimeOfAdd(res->getInt("time"));
            t.setTestTable(res->getString("test_table"));
            t.setNumOfRuns(res->getInt("num_of_runs"));
            t.setRerun(res->getBoolean("rerun"));
            t.setTimeOfRerun(res->getInt("time_rr"));
            t.setReturnValue(res->getInt("return_value"));
            l.push_back(t);
        }
        freeResources(connection, preparedStmt, res);
        t.insert(t.end(), l.begin(), l.end());
        return true;
    }catch(exception& ex) {
        logger->logError("getTestsNotFinished " + string(ex.what()));
        freeResources(connection, preparedStmt, res);
        return false;
    }
}

bool MySqlTestManager::setTestHasFinished(Test t)
{
    Connection* connection = nullptr;
    PreparedStatement* preparedStmt = nullptr;
    try {
        while((connection = dbPool->getConnectionFromPool()) == nullptr)
            std::this_thread::sleep_for(std::chrono::milliseconds(1));
        preparedStmt = connection->prepareStatement("UPDATE tests SET num_of_runs = ?, rerun = 0, return_value = ?, ended = 1 WHERE id = ?;");
        preparedStmt->setInt(1,t.getNumOfRuns());
        preparedStmt->setInt(2,t.getReturnValue());
        preparedStmt->setInt64(3, t.getId());
        int count = preparedStmt->executeUpdate();
        if (preparedStmt != nullptr)
            delete preparedStmt;
        dbPool->releaseConnection(connection);
        return count == 1 ? true : false;
    }catch(exception& ex) {
        logger->logError("setTestHasFinished " + string(ex.what()));
        if (preparedStmt != nullptr)
            delete preparedStmt;
        if (connection != nullptr)
            dbPool->releaseConnection(connection);
        return false;
    }
}

bool MySqlTestManager::setTestAsLoaded(const Test &t)
{
    Connection* connection = nullptr;
    PreparedStatement* preparedStmt = nullptr;
    try {
        while((connection = dbPool->getConnectionFromPool()) == nullptr)
            std::this_thread::sleep_for(std::chrono::milliseconds(1));
        preparedStmt = connection->prepareStatement("UPDATE tests SET loaded = ? WHERE id = ? AND loaded = ?;");
        preparedStmt->setInt(1,1);
        preparedStmt->setInt(2,t.getId());
        preparedStmt->setInt(3,0);
        int count = preparedStmt->executeUpdate();
        if (preparedStmt != nullptr)
            delete preparedStmt;
        dbPool->releaseConnection(connection);
        return count == 1 ? true : false;
    }catch(exception& ex) {
        logger->logError("setTestAsLoaded " + string(ex.what()));
        if (preparedStmt != nullptr)
            delete preparedStmt;
        if (connection != nullptr)
            dbPool->releaseConnection(connection);
        return false;
    }
}

bool MySqlTestManager::setTestAsLoadedForRerun(const Test &t)
{
    Connection* connection = nullptr;
    PreparedStatement* preparedStmt = nullptr;
    try {
        while((connection = dbPool->getConnectionFromPool()) == nullptr)
            std::this_thread::sleep_for(std::chrono::milliseconds(1));
        preparedStmt = connection->prepareStatement("UPDATE tests SET loaded_for_rerun = 1 WHERE id = ?;");
        preparedStmt->setInt64(1, t.getId());
        int count = preparedStmt->executeUpdate();
        if (preparedStmt != nullptr)
            delete preparedStmt;
        dbPool->releaseConnection(connection);
        return count == 1 ? true : false;
    }catch(exception& ex) {
        logger->logError("setTestAsLoadedForRerun " + string(ex.what()));
        if (preparedStmt != nullptr)
            delete preparedStmt;
        if (connection != nullptr)
            dbPool->releaseConnection(connection);
        return false;
    }
}

bool MySqlTestManager::updateTestForRerun(const Test &t)
{
    Connection* connection = nullptr;
    PreparedStatement* preparedStmt = nullptr;
    try {
        while((connection = dbPool->getConnectionFromPool()) == nullptr)
            std::this_thread::sleep_for(std::chrono::milliseconds(1));
        preparedStmt = connection->prepareStatement("UPDATE tests SET num_of_runs = ?, rerun = 1, time_of_rerun = FROM_UNIXTIME(?), loaded_for_rerun = 0, return_value = ? WHERE id = ?;");
        preparedStmt->setInt(1,t.getNumOfRuns());
        preparedStmt->setInt(2,t.getTimeOfRerun());
        preparedStmt->setInt(3,t.getReturnValue());
        preparedStmt->setInt64(4, t.getId());
        int count = preparedStmt->executeUpdate();
        if (preparedStmt != nullptr)
            delete preparedStmt;
        dbPool->releaseConnection(connection);
        return count == 1 ? true : false;
    }catch(exception& ex) {
        logger->logError("updateTestForRerun " + string(ex.what()));
        if (preparedStmt != nullptr)
            delete preparedStmt;
        if (connection != nullptr)
            dbPool->releaseConnection(connection);
        return false;
    }
}

void MySqlTestManager::freeResources(Connection* con, PreparedStatement* p, ResultSet* r)
{
    if (p != nullptr)
        delete p;
    if (r != nullptr)
        delete r;
    if (con != nullptr)
        dbPool->releaseConnection(con);
}
