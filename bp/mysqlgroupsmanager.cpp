#include "mysqlgroupsmanager.h"

#include <stdexcept>
#include <cppconn/driver.h>
#include <cppconn/driver.h>
#include <cppconn/resultset.h>
#include <cppconn/prepared_statement.h>

using namespace std;
using namespace sql;

MySqlGroupsManager::MySqlGroupsManager(MySqlDBPool *pool) :
    logger(new Logger()), dbPool(pool) {}

bool MySqlGroupsManager::increaseFinishedTests(Test t)
{
    Connection* connection = nullptr;
    PreparedStatement* preparedStmt = nullptr;
    ResultSet* res = nullptr;
    try {
        while((connection = dbPool->getConnectionFromPool()) == nullptr)
            std::this_thread::sleep_for(std::chrono::milliseconds(1));
        preparedStmt = connection->prepareStatement("SELECT id FROM groups_tests WHERE id_test = ?;");
        preparedStmt->setInt64(1, t.getId());
        res = preparedStmt->executeQuery();
        int i = 0;
        long group_id;
        while(res->next()) {
            group_id = res->getInt64("id");
            i++;
        }
        if (i != 1)
            return false;
        if (res)
            delete res;
        if (preparedStmt)
            delete preparedStmt;
        preparedStmt = connection->prepareStatement("UPDATE groups SET finished_tests = finished_tests + 1 WHERE id = ?;");
        preparedStmt->setInt(1, group_id);
        i = preparedStmt->executeUpdate();
        if (preparedStmt != nullptr)
            delete preparedStmt;
        dbPool->releaseConnection(connection);
        return true;
    }catch(exception& ex) {
        logger->logError("MySqlGroupsManager::increaseFinishedTests " + string(ex.what()));
        if (preparedStmt != nullptr)
            delete preparedStmt;
        if (connection != nullptr)
            dbPool->releaseConnection(connection);
        return false;
    }
}
