#ifndef MYSQLTESTMANAGER_H
#define MYSQLTESTMANAGER_H
#include "itestmanager.h"
#include <list>
#include "mysql_connection.h"
#include "configstorage.h"
#include "ilogger.h"
#include "mysqldbpool.h"
#include <cppconn/driver.h>
#include <cppconn/resultset.h>
#include <cppconn/prepared_statement.h>

/**
 * @brief The MySqlTestManager class implements interface ITestManager. For methods
 * documentation see interface.
 */
class MySqlTestManager : public ITestManager
{
private:
    ILogger* logger = nullptr;
    MySqlDBPool* dbPool = nullptr;
public:
    MySqlTestManager(MySqlDBPool* pool);
    ~MySqlTestManager();
    virtual bool getAllTestsReadyForRunning(std::list<Test>& t) override;
    virtual bool getTestsNotFinished(std::list<Test>& t) override;
    virtual bool setTestHasFinished(Test t) override;
    virtual bool setTestAsLoaded(const Test& t) override;
    virtual bool updateTestForRerun(const Test& t) override;
    virtual bool setTestAsLoadedForRerun(const Test &t) override;
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

#endif // MYSQLTESTMANAGER_H
