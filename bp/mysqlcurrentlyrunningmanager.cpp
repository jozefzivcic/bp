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

extern mutex dbMutex;

MySqlCurrentlyRunningManager::MySqlCurrentlyRunningManager(const ConfigStorage *storage)
{
    logger = new Logger();
    dbMutex.lock();
    driver = get_driver_instance();
    dbMutex.unlock();
    driver->threadInit();
    _con = driver->connect(storage->getDatabase(), storage->getUserName(), storage->getUserPassword());
    _con->setSchema(storage->getSchema());
}

MySqlCurrentlyRunningManager::~MySqlCurrentlyRunningManager()
{
    if (_con != nullptr)
        delete _con;
    if (logger != nullptr)
        delete logger;
    driver->threadEnd();
}

bool MySqlCurrentlyRunningManager::insertTest(Test t)
{
    PreparedStatement* preparedStmt = nullptr;
    try {
        preparedStmt = _con->prepareStatement("INSERT INTO currently_running (id_test) VALUES (?);");
        preparedStmt->setInt(1,t.id());
        preparedStmt->execute();
        if (preparedStmt != nullptr)
            delete preparedStmt;
        return true;
    }catch(exception& ex) {
        logger->logError("insertTest " + string(ex.what()));
        if (preparedStmt != nullptr)
            delete preparedStmt;
        return false;
    }
}

bool MySqlCurrentlyRunningManager::removeTest(Test t)
{
    PreparedStatement* preparedStmt = nullptr;
    try {
        preparedStmt = _con->prepareStatement("DELETE FROM currently_running WHERE id_test = ?;");
        preparedStmt->setInt(1,t.id());
        preparedStmt->execute();
        if (preparedStmt != nullptr)
            delete preparedStmt;
        return true;
    }catch(exception& ex) {
        logger->logError("removeTest " + string(ex.what()));
        if (preparedStmt != nullptr)
            delete preparedStmt;
        return false;
    }
}
