#include "mysqlchangestatemanager.h"
#include "constants.h"
using namespace std;
using namespace sql;

MySqlChangeStateManager::MySqlChangeStateManager()
{
    Driver *driver;
    driver = get_driver_instance();
    connection = driver->connect(Constants::DATABASE, Constants::USERNAME, Constants::USER_PASSWORD);
    connection->setSchema(Constants::SCHEMA);
}

MySqlChangeStateManager::~MySqlChangeStateManager()
{
    if (connection != nullptr)
        delete connection;
}

bool MySqlChangeStateManager::getDBState(int& state)
{
    PreparedStatement* preparedStmt;
    ResultSet* res;
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
