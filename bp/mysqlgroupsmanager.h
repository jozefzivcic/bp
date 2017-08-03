#ifndef MYSQLGROUPSMANAGER_H
#define MYSQLGROUPSMANAGER_H

#include "mysqldbpool.h"
#include "igroupsmanager.h"

/**
 * @brief The MySqlGroupsManager class implements interface IGroupsManager. If
 * you wish to see documentation, please see documentation for interface.
 */
class MySqlGroupsManager : public IGroupsManager
{
private:
    ILogger* logger = nullptr;
    MySqlDBPool* dbPool = nullptr;
public:

    MySqlGroupsManager(MySqlDBPool* pool);
    ~MySqlGroupsManager();
    virtual bool increaseFinishedTests(Test t) override;
};

#endif // MYSQLGROUPSMANAGER_H
