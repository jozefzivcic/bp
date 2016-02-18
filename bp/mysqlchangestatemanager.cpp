#include "mysqlchangestatemanager.h"
#include <mutex>
using namespace std;
using namespace sql;

extern mutex dbMutex;
MySqlChangeStateManager::MySqlChangeStateManager(const ConfigStorage *storage)
{
    Driver *driver;
    dbMutex.lock();
    driver = get_driver_instance();
    dbMutex.unlock();
    connection = driver->connect(storage->getDatabase(), storage->getUserName(), storage->getUserPassword());
    connection->setSchema(storage->getSchema());
}

MySqlChangeStateManager::~MySqlChangeStateManager()
{
    if (connection != nullptr)
        delete connection;
}

bool MySqlChangeStateManager::getDBState(int& state)
{
    PreparedStatement* preparedStmt = nullptr;
    ResultSet* res = nullptr;
    try{
        preparedStmt = connection->prepareStatement("SELECT change_number FROM change_table WHERE id = ?;");
        preparedStmt->setInt(0,0);
        int i = 0;
        int tempState = 0;
        res = preparedStmt->executeQuery();
        while(res->next()) {
            tempState = res->getInt("change_number");
            i++;
        }
        deleteStatementAndResSet(preparedStmt,res);
        if (i != 1)
            return false;
        state = tempState;
        return true;
    }catch(exception) {
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
