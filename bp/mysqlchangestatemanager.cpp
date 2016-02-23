#include "mysqlchangestatemanager.h"
#include <mutex>
using namespace std;
using namespace sql;

extern mutex dbMutex;
MySqlChangeStateManager::MySqlChangeStateManager(const ConfigStorage *storage)
{
    logger = new Logger();
    dbMutex.lock();
    driver = get_driver_instance();
    dbMutex.unlock();
    driver->threadInit();
    connection = driver->connect(storage->getDatabase(), storage->getUserName(), storage->getUserPassword());
    connection->setSchema(storage->getSchema());
}

MySqlChangeStateManager::~MySqlChangeStateManager()
{
    if (connection != nullptr)
        delete connection;
    if (logger != nullptr)
        delete logger;
    driver->threadEnd();
}

bool MySqlChangeStateManager::getDBState(int& state)
{
    PreparedStatement* preparedStmt = nullptr;
    ResultSet* res = nullptr;
    try{
        preparedStmt = connection->prepareStatement("SELECT change_number FROM change_table WHERE id = ?;");
        preparedStmt->setInt(1,0);
        int i = 0;
        int tempState = 0;
        res = preparedStmt->executeQuery();
        while(res->next()) {
            tempState = res->getInt("change_number");
            i++;
        }
        deleteStatementAndResSet(preparedStmt,res);
        if (i != 1) {
            logger->logError("getDBState: More rows selected");
            return false;
        }
        state = tempState;
        return true;
    }catch(exception& ex) {
        logger->logError("getDBState " + string(ex.what()));
        deleteStatementAndResSet(preparedStmt,res);
        return false;
    }
}

void MySqlChangeStateManager::deleteStatementAndResSet(PreparedStatement* p, ResultSet* r)
{
    if (p != nullptr)
        delete p;
    if (r != nullptr)
        delete r;
}
