#ifndef MYSQLTESTMANAGER_H
#define MYSQLTESTMANAGER_H
#include "itestmanager.h"
#include <list>
#include "mysql_connection.h"
#include "configstorage.h"
#include "ilogger.h"
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
    sql::Driver *driver;
    sql::Connection* _con = nullptr;
    ILogger* logger = nullptr;
public:
    MySqlTestManager(const ConfigStorage* storage);
    ~MySqlTestManager();
    virtual bool getAllTestsReadyForRunning(std::list<Test>& t) override;
    virtual bool getTestsNotFinished(std::list<Test>& t) override;
    //virtual bool setTestHasStarted(Test t) override;
    virtual bool setTestHasFinished(Test t) override;
    virtual bool setTestAsLoaded(const Test& t) override;
private:

    /**
     * @brief deleteStatementAndResSet If PreparedStatement or ResultSet is not nullptr,
     * then frees them.
     * @param p PreparedStatement to be freed.
     * @param r ResultSet to be freed.
     */
    void deleteStatementAndResSet(sql::PreparedStatement* p, sql::ResultSet* r);
};

#endif // MYSQLTESTMANAGER_H
