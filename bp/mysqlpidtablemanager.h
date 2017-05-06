#ifndef MYSQLPIDTABLEMANAGER_H
#define MYSQLPIDTABLEMANAGER_H
#include "ilogger.h"
#include "ipidtablemanager.h"
#include "mysqldbpool.h"
#include <cppconn/resultset.h>

/**
 * @brief The MySqlPIDTableManager class implements interface IPIDTableManager. For methods documentation see
 * the interface.
 */
class MySqlPIDTableManager : public IPIDTableManager
{
private:
    ILogger* logger = nullptr;
    MySqlDBPool* dbPool = nullptr;
public:
    MySqlPIDTableManager(MySqlDBPool* pool);
    ~MySqlPIDTableManager();
    virtual bool storePIDForId(long id, int pid) override;
    virtual bool removePIDForId(long id) override;
    virtual bool getPIDForId(long id, pid_t& pid) override;
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

#endif // MYSQLPIDTABLEMANAGER_H
