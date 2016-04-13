#ifndef MYSQLCHANGESTATEMANAGER_H
#define MYSQLCHANGESTATEMANAGER_H
#include "ichangestatemanager.h"
#include "mysql_connection.h"
#include "configstorage.h"
#include "ilogger.h"
#include "logger.h"
#include "mysqldbpool.h"
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
    ILogger* logger = nullptr;
    MySqlDBPool* dbPool;
public:
    MySqlChangeStateManager(MySqlDBPool* pool);
    ~MySqlChangeStateManager();
    virtual bool getDBState(long &state) override;
private:

    /**
     * @brief freeResources If con is not nullptr, then this method returns it into pool
     * and if PreparedStatement or ResultSet is not nullptr, then frees them.
     * @param con Connection to be returned to pool.
     * @param p PreparedStatement to be freed.
     * @param r ResultSet to be freed.
     */
    void freeResources(sql::Connection* con, sql::PreparedStatement* p, sql::ResultSet* r);
};

#endif // MYSQLCHANGESTATEMANAGER_H
