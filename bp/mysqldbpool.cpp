#include "mysqldbpool.h"
#include "logger.h"
#include <cppconn/exception.h>
#include <cppconn/prepared_statement.h>

using namespace std;
using namespace sql;

MySqlDBPool::MySqlDBPool(string db, string usr, string passwd) :
    database(db), user(usr), password(passwd), isSchema(false)
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

MySqlDBPool::MySqlDBPool(string db, string usr, string passwd, string databaseSchema) :
    database(db), user(usr), password(passwd), schema(databaseSchema), isSchema(true)
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
        if (password != "no")
            con = driver->connect(database, user, password);
        else {
            ConnectOptionsMap com;
            com["database"] = database;
            com["user"] = user;
            con = driver->connect(com);
        }
        if (isSchema)
            con->setSchema(schema);
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

bool MySqlDBPool::pingConnection(sql::Connection *con)
{
    PreparedStatement* preparedStmt = nullptr;
    try{
        preparedStmt = con->prepareStatement("SELECT 0 FROM dual;");
        preparedStmt->execute();
        if (preparedStmt != nullptr)
            delete preparedStmt;
        return true;
    }catch(exception& ex) {
        if (preparedStmt != nullptr)
            delete preparedStmt;
        logger->logError("pingConnection " + string(ex.what()));
        return false;
    }
}

