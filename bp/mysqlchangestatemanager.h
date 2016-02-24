#ifndef MYSQLCHANGESTATEMANAGER_H
#define MYSQLCHANGESTATEMANAGER_H
#include "ichangestatemanager.h"
#include "mysql_connection.h"
#include "configstorage.h"
#include "ilogger.h"
#include "logger.h"
#include <cppconn/driver.h>
#include <cppconn/resultset.h>
#include <cppconn/prepared_statement.h>

/**
 * @brief The MySqlChangeStateManager class implements interface IChangeStateManager. For
 * methods documentation see interface.
 */
class MySqlChangeStateManager : public IChangeStateManager
{
private:
    sql::Driver *driver;
    sql::Connection* connection = nullptr;
    ILogger* logger = nullptr;
public:
    MySqlChangeStateManager(const ConfigStorage* storage);
    ~MySqlChangeStateManager();
    virtual bool getDBState(int& state) override;
private:

    /**
     * @brief deleteStatementAndResSet If PreparedStatement or ResultSet is not nullptr,
     * then frees them.
     * @param p PreparedStatement to be freed.
     * @param r ResultSet to be freed.
     */
    void deleteStatementAndResSet(sql::PreparedStatement* p, sql::ResultSet* r);
};

#endif // MYSQLCHANGESTATEMANAGER_H
