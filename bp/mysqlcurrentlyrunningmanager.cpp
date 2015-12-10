#include "mysqlcurrentlyrunningmanager.h"
#include "mysql_connection.h"
#include <cppconn/driver.h>
#include <cppconn/exception.h>
#include <cppconn/resultset.h>
#include <cppconn/prepared_statement.h>
#include "constants.h"
#include <stdexcept>

using namespace std;
using namespace sql;

MySqlCurrentlyRunningManager::MySqlCurrentlyRunningManager()
{
    Driver *driver;
    driver = get_driver_instance();
    _con = driver->connect(Constants::DATABASE, Constants::USERNAME, Constants::USER_PASSWORD);
    _con->setSchema(Constants::SCHEMA);
}

MySqlCurrentlyRunningManager::~MySqlCurrentlyRunningManager()
{
    if (_con != nullptr)
        delete _con;
}

bool MySqlCurrentlyRunningManager::insertTest(Test t)
{
    PreparedStatement* preparedStmt;
    try {
        preparedStmt = _con->prepareStatement("INSERT INTO currently_running (id_test) VALUES (?);");
        preparedStmt->setInt(1,t.id());
        preparedStmt->execute();
        if (preparedStmt != nullptr)
            delete preparedStmt;
        return true;
    }catch(exception) {
        if (preparedStmt != nullptr)
            delete preparedStmt;
        return false;
    }
}

bool MySqlCurrentlyRunningManager::removeTest(Test t)
{
    PreparedStatement* preparedStmt;
    try {
        preparedStmt = _con->prepareStatement("DELETE FROM currently_running WHERE id_test = ?;");
        preparedStmt->setInt(1,t.id());
        preparedStmt->execute();
        if (preparedStmt != nullptr)
            delete preparedStmt;
        return true;
    }catch(exception) {
        if (preparedStmt != nullptr)
            delete preparedStmt;
        return false;
    }
}
