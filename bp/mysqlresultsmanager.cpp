#include "mysqlresultsmanager.h"
#include <cppconn/driver.h>
#include <mutex>
#include "logger.h"

using namespace std;
using namespace sql;

extern mutex dbMutex;

MySqlResultsManager::MySqlResultsManager(const ConfigStorage *storage)
{
    logger = new Logger();
    dbMutex.lock();
    driver = get_driver_instance();
    dbMutex.unlock();
    driver->threadInit();
    connection = driver->connect(storage->getDatabase(), storage->getUserName(), storage->getUserPassword());
    connection->setSchema(storage->getSchema());
}

MySqlResultsManager::~MySqlResultsManager()
{
    if (connection != nullptr)
        delete connection;
    if (logger != nullptr)
        delete logger;
    driver->threadEnd();
}

bool MySqlResultsManager::storePathForTest(Test t, string path)
{
    PreparedStatement* preparedStmt = nullptr;
    try {
        preparedStmt = connection->prepareStatement("INSERT INTO results (id_test, directory) VALUES (?,?);");
        preparedStmt->setInt(1,t.getId());
        preparedStmt->setString(2, path);
        preparedStmt->execute();
        if (preparedStmt != nullptr)
            delete preparedStmt;
        return true;
    }catch(exception& ex) {
        logger->logError("storePathForTest " + string(ex.what()));
        if (preparedStmt != nullptr)
            delete preparedStmt;
        return false;
    }
}

