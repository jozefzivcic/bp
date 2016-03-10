#include "mysqldbpool.h"
#include "logger.h"
#include <cppconn/exception.h>

using namespace std;
using namespace sql;

MySqlDBPool::MySqlDBPool(string db, string usr, string passwd) :
    database(db), user(usr), password(passwd)
{
    logger = new Logger();
    try {
        driver = get_driver_instance();
        driver->threadInit();
    }catch(SQLException& ex) {
        logger->logError("MySqlDBPool::MySqlDBPool " + string(ex.what()));
        throw;
    }
}

MySqlDBPool::~MySqlDBPool()
{
    driver->threadEnd();
    if (logger != nullptr)
        delete logger;
}

Connection *MySqlDBPool::createConnection()
{
    Connection* con;
    try {
        con = driver->connect(database, user, password);
        con->setSchema("mydb");
        return con;
    }catch(SQLException& ex) {
        logger->logError("MySqlDBPool::createConnection " + string(ex.what()));
        return nullptr;
    }

}

bool MySqlDBPool::deleteConnection(sql::Connection *con)
{
    if (con == nullptr)
        return false;
    delete con;
    return true;
}

