#ifndef MYSQLDBPOOL_H
#define MYSQLDBPOOL_H
#include "generaldbpool.h"
#include "mysql_connection.h"
#include <cppconn/driver.h>
#include "ilogger.h"

class MySqlDBPool : public GeneralDBPool<sql::Connection>
{
private:
    std::string database;
    std::string user;
    std::string password;
    std::string schema;
    bool isSchema;
    sql::Driver* driver;
    ILogger* logger = nullptr;
public:
    MySqlDBPool(std::string db, std::string usr, std::string passwd);
    MySqlDBPool(std::string db, std::string usr, std::string passwd, std::string databaseSchema);
    ~MySqlDBPool();
    virtual sql::Connection* createConnection() override;

    virtual bool deleteConnection(sql::Connection *con) override;

    virtual bool pingConnection(sql::Connection *con) override;
};

#endif // MYSQLDBPOOL_H
