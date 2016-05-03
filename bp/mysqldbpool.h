#ifndef MYSQLDBPOOL_H
#define MYSQLDBPOOL_H
#include "generaldbpool.h"
#include "mysql_connection.h"
#include <cppconn/driver.h>
#include "ilogger.h"

/**
 * @brief The MySqlDBPool class extends abstract class GeneralDBPool. For methods info see base class.
 */
class MySqlDBPool : public GeneralDBPool<sql::Connection>
{
private:

    /**
     * @brief database Name of database.
     */
    std::string database;

    /**
     * @brief user User that is used to connect to the database.
     */
    std::string user;

    /**
     * @brief password User password.
     */
    std::string password;

    /**
     * @brief schema Database schema.
     */
    std::string schema;

    /**
     * @brief isSchema If pool was created with schema and all new connections should have set schema.
     */
    bool isSchema;

    /**
     * @brief driver Database driver.
     */
    sql::Driver* driver;

    /**
     * @brief logger Logging class.
     */
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
