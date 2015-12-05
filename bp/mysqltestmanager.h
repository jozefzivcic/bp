#ifndef MYSQLTESTMANAGER_H
#define MYSQLTESTMANAGER_H
#include "itestmanager.h"
#include <list>
#include "mysql_connection.h"
#include <cppconn/driver.h>
#include <cppconn/resultset.h>
#include <cppconn/prepared_statement.h>

class MySqlTestManager : public ITestManager
{
private:
    sql::Connection* _con;
public:
    MySqlTestManager();
    ~MySqlTestManager();
    virtual std::list<Test> getAllTestsReadyForRunning() override;
    virtual bool setTestHasStarted(Test t) override;
    virtual bool setTestHasFinished(Test t) override;
private:
    void deleteStatementAndResSet(sql::PreparedStatement* p, sql::ResultSet* r);
};

#endif // MYSQLTESTMANAGER_H