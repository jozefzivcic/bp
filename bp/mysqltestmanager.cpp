#include "mysqltestmanager.h"
#include "constants.h"
#include <cppconn/driver.h>

using namespace std;
using namespace sql;
MySqlTestManager::MySqlTestManager()
{
    Driver *driver;
    driver = get_driver_instance();
    _con = driver->connect(Constants::DATABASE, Constants::USERNAME, Constants::USER_PASSWORD);
    _con->setSchema(Constants::SCHEMA);
}

MySqlTestManager::~MySqlTestManager()
{
    if (_con != nullptr)
        delete _con;
}

bool MySqlTestManager::getAllTestsReadyForRunning(list<Test>& t)
{
    PreparedStatement* preparedStmt;
    ResultSet* res;
    list<Test> l;
    try{
        preparedStmt = _con->prepareStatement("SELECT id, id_file, id_user, UNIX_TIMESTAMP(time_of_add) time, test_table FROM tests WHERE loaded = 0 AND run = 0;");
        res = preparedStmt->executeQuery();
        while(res->next()) {
            Test t;
            t.setId(res->getInt("id"));
            t.setIdFile(res->getInt("id_file"));
            t.setIdUser(res->getInt("id_user"));
            t.setTimeOfAdd(res->getInt("time"));
            t.setTestTable(res->getString("test_table"));
            l.push_back(t);
        }
        deleteStatementAndResSet(preparedStmt,res);
        for (Test test : l) {
            setTestAsLoaded(test);
        }
        t.insert(t.end(), l.begin(), l.end());
        return true;
    }catch(exception) {
        deleteStatementAndResSet(preparedStmt,res);
        return false;
    }
}

bool MySqlTestManager::setTestHasStarted(Test t)
{
    PreparedStatement* preparedStmt;
    try {
        preparedStmt = _con->prepareStatement("UPDATE tests SET run = ?, ended = ? WHERE id = ?;");
        preparedStmt->setInt(1,1);
        preparedStmt->setInt(2,0);
        preparedStmt->setInt(3,t.id());
        int count = preparedStmt->executeUpdate();
        if (preparedStmt != nullptr)
            delete preparedStmt;
        return count == 1 ? true : false;
    }catch(exception) {
        if (preparedStmt != nullptr)
            delete preparedStmt;
        return false;
    }
}

bool MySqlTestManager::setTestHasFinished(Test t)
{
    PreparedStatement* preparedStmt;
    try {
        preparedStmt = _con->prepareStatement("UPDATE tests SET ended = ? WHERE id = ? AND run = ?;");
        preparedStmt->setInt(1,1);
        preparedStmt->setInt(2,t.id());
        preparedStmt->setInt(3,1);
        int count = preparedStmt->executeUpdate();
        if (preparedStmt != nullptr)
            delete preparedStmt;
        return count == 1 ? true : false;
    }catch(exception) {
        if (preparedStmt != nullptr)
            delete preparedStmt;
        return false;
    }
}

bool MySqlTestManager::setTestAsLoaded(const Test &t)
{
    PreparedStatement* preparedStmt;
    try {
        preparedStmt = _con->prepareStatement("UPDATE tests SET loaded = ? WHERE id = ? AND loaded = ?;");
        preparedStmt->setInt(1,1);
        preparedStmt->setInt(2,t.id());
        preparedStmt->setInt(3,0);
        int count = preparedStmt->executeUpdate();
        if (preparedStmt != nullptr)
            delete preparedStmt;
        return count == 1 ? true : false;
    }catch(exception) {
        if (preparedStmt != nullptr)
            delete preparedStmt;
        return false;
    }
}

void MySqlTestManager::deleteStatementAndResSet(PreparedStatement* p, ResultSet* r)
{
    if (p != nullptr)
        delete p;
    if (r != nullptr)
        delete r;
}
