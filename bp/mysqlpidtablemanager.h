#ifndef MYSQLPIDTABLEMANAGER_H
#define MYSQLPIDTABLEMANAGER_H
#include "ilogger.h"
#include "ipidtablemanager.h"
#include "mysqldbpool.h"

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
    virtual bool storePIDForId(int id, int pid) override;
    virtual bool removePIDForId(int id) override;
};

#endif // MYSQLPIDTABLEMANAGER_H
