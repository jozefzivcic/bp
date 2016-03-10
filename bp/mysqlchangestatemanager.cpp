#include "mysqlchangestatemanager.h"
#include <mutex>
using namespace std;
using namespace sql;

extern mutex dbMutex;
MySqlChangeStateManager::MySqlChangeStateManager(MySqlDBPool *pool)
{
    logger = new Logger();
    dbPool = pool;
}

MySqlChangeStateManager::~MySqlChangeStateManager()
{
    if (logger != nullptr)
        delete logger;
}

bool MySqlChangeStateManager::getDBState(int& state)
{
    Connection* connection = nullptr;
    PreparedStatement* preparedStmt = nullptr;
    ResultSet* res = nullptr;
    try{
        connection = dbPool->getConnectionFromPoolBusy();
        preparedStmt = connection->prepareStatement("SELECT change_number FROM change_table WHERE id = ?;");
        preparedStmt->setInt(1,0);
        int i = 0;
        int tempState = 0;
        res = preparedStmt->executeQuery();
        while(res->next()) {
            tempState = res->getInt("change_number");
            i++;
        }
        freeResources(connection, preparedStmt, res);
        if (i != 1) {
            logger->logError("getDBState: More rows selected");
            return false;
        }
        state = tempState;
        return true;
    }catch(exception& ex) {
        logger->logError("getDBState " + string(ex.what()));
        freeResources(connection, preparedStmt, res);
        return false;
    }
}

void MySqlChangeStateManager::freeResources(Connection* con, PreparedStatement* p, ResultSet* r)
{
    if (con != nullptr)
        dbPool->releaseConnection(con);
    if (p != nullptr)
        delete p;
    if (r != nullptr)
        delete r;
}
