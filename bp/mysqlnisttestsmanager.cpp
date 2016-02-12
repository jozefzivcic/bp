#include "mysqlnisttestsmanager.h"
#include <cppconn/driver.h>
#include <cppconn/resultset.h>
#include <cppconn/prepared_statement.h>

using namespace std;
using namespace sql;

MySqlNistTestsManager::MySqlNistTestsManager(const ConfigStorage *storage)
{
    Driver *driver;
    driver = get_driver_instance();
    connection = driver->connect(storage->getDatabase(), storage->getUserName(), storage->getUserPassword());
    connection->setSchema(storage->getSchema());
}

MySqlNistTestsManager::~MySqlNistTestsManager()
{
    if (connection != nullptr)
        delete connection;
}

bool MySqlNistTestsManager::getParameterById(long id, NistTestParameter &param)
{

}

