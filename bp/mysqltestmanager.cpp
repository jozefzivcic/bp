#include "mysqltestmanager.h"
#include "logger.h"
#include <cppconn/driver.h>
#include <mutex>

using namespace std;
using namespace sql;

extern mutex dbMutex;

MySqlTestManager::MySqlTestManager(const ConfigStorage *storage)
{
    logger = new Logger();
    dbMutex.lock();
    driver = get_driver_instance();
    dbMutex.unlock();
    driver->threadInit();
    _con = driver->connect(storage->getDatabase(), storage->getUserName(), storage->getUserPassword());
    _con->setSchema(storage->getSchema());
}
MySqlTestManager::~MySqlTestManager()
{
    if (_con != nullptr)
        delete _con;
    if (logger != nullptr)
        delete logger;
    driver->threadEnd();
}

bool MySqlTestManager::getAllTestsReadyForRunning(list<Test>& t)
{
    PreparedStatement* preparedStmt = nullptr;
    ResultSet* res = nullptr;
    list<Test> l;
    try{
        preparedStmt = _con->prepareStatement("SELECT id, id_file, id_user, UNIX_TIMESTAMP(time_of_add) time, test_table FROM tests WHERE loaded = 0;");
        res = preparedStmt->executeQuery();
        while(res->next()) {
            Test t;
            t.setId(res->getInt("id"));
            t.setIdFile(res->getInt("id_file"));
            t.setIdUser(res->getInt("id_user"));
            t.setTimeOfAdd(res->getInt("time"));
            t.setTestTable(res->getString("test_table"));
            l.push_back(t);
        }
        deleteStatementAndResSet(preparedStmt,res);
        t.insert(t.end(), l.begin(), l.end());
        return true;
    }catch(exception& ex) {
        logger->logError("getAllTestsReadyForRunning " + string(ex.what()));
        deleteStatementAndResSet(preparedStmt,res);
        return false;
    }
}

bool MySqlTestManager::getTestsNotFinished(std::list<Test> &t)
{
    PreparedStatement* preparedStmt = nullptr;
    ResultSet* res = nullptr;
    list<Test> l;
    try{
        preparedStmt = _con->prepareStatement("SELECT id, id_file, id_user, UNIX_TIMESTAMP(time_of_add) time, test_table FROM tests WHERE loaded = 1 AND ended = 0;");
        res = preparedStmt->executeQuery();
        while(res->next()) {
            Test t;
            t.setId(res->getInt("id"));
            t.setIdFile(res->getInt("id_file"));
            t.setIdUser(res->getInt("id_user"));
            t.setTimeOfAdd(res->getInt("time"));
            t.setTestTable(res->getString("test_table"));
            l.push_back(t);
        }
        deleteStatementAndResSet(preparedStmt,res);
        t.insert(t.end(), l.begin(), l.end());
        return true;
    }catch(exception& ex) {
        logger->logError("getTestsNotFinished " + string(ex.what()));
        deleteStatementAndResSet(preparedStmt,res);
        return false;
    }
}
/*
bool MySqlTestManager::setTestHasStarted(Test t)
{
    PreparedStatement* preparedStmt;
    try {
        preparedStmt = _con->prepareStatement("UPDATE tests SET run = ?, ended = ? WHERE id = ?;");
        preparedStmt->setInt(1,1);
        preparedStmt->setInt(2,0);
        preparedStmt->setInt(3,t.id());
        int count = preparedStmt->executeUpdate();
        if (preparedStmt != nullptr)
            delete preparedStmt;
        return count == 1 ? true : false;
    }catch(exception) {
        if (preparedStmt != nullptr)
            delete preparedStmt;
        return false;
    }
}
*/
bool MySqlTestManager::setTestHasFinished(Test t)
{
    PreparedStatement* preparedStmt = nullptr;
    try {
        preparedStmt = _con->prepareStatement("UPDATE tests SET ended = ? WHERE id = ?;");
        preparedStmt->setInt(1,1);
        preparedStmt->setInt(2,t.id());
        int count = preparedStmt->executeUpdate();
        if (preparedStmt != nullptr)
            delete preparedStmt;
        return count == 1 ? true : false;
    }catch(exception& ex) {
        logger->logError("setTestHasFinished " + string(ex.what()));
        if (preparedStmt != nullptr)
            delete preparedStmt;
        return false;
    }
}

bool MySqlTestManager::setTestAsLoaded(const Test &t)
{
    PreparedStatement* preparedStmt = nullptr;
    try {
        preparedStmt = _con->prepareStatement("UPDATE tests SET loaded = ? WHERE id = ? AND loaded = ?;");
        preparedStmt->setInt(1,1);
        preparedStmt->setInt(2,t.id());
        preparedStmt->setInt(3,0);
        int count = preparedStmt->executeUpdate();
        if (preparedStmt != nullptr)
            delete preparedStmt;
        return count == 1 ? true : false;
    }catch(exception& ex) {
        logger->logError("setTestAsLoaded " + string(ex.what()));
        if (preparedStmt != nullptr)
            delete preparedStmt;
        return false;
    }
}

void MySqlTestManager::deleteStatementAndResSet(PreparedStatement* p, ResultSet* r)
{
    if (p != nullptr)
        delete p;
    if (r != nullptr)
        delete r;
}
