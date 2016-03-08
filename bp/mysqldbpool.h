#ifndef MYSQLDBPOOL_H
#define MYSQLDBPOOL_H
#include "generaldbpool.h"
#include "mysql_connection.h"

class MySqlDBPool : public GeneralDBPool<sql::Connection>
{
private:
    std::string database;
    std::string user;
    std::string password;
public:
    MySqlDBPool(std::string db, std::string usr, std::string passwd);
    virtual sql::Connection* createConnection() override;

    virtual bool deleteConnection(sql::Connection *con) override;
};

#endif // MYSQLDBPOOL_H
