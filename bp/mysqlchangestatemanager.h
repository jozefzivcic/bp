#ifndef MYSQLCHANGESTATEMANAGER_H
#define MYSQLCHANGESTATEMANAGER_H
#include "ichangestatemanager.h"
#include "mysql_connection.h"
#include <cppconn/driver.h>
#include <cppconn/resultset.h>
#include <cppconn/prepared_statement.h>

class MySqlChangeStateManager : public IChangeStateManager
{
private:
    sql::Connection* connection;
public:
    MySqlChangeStateManager();
    ~MySqlChangeStateManager();
    virtual bool getDBState(int& state) override;
private:
    void deleteStatementAndResSet(sql::PreparedStatement* p, sql::ResultSet* r);
};

#endif // MYSQLCHANGESTATEMANAGER_H
