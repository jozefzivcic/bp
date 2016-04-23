#include "mysqlnisttestsmanager.h"
#include "logger.h"
#include <cppconn/driver.h>
#include <mutex>

using namespace std;
using namespace sql;

MySqlNistTestsManager::MySqlNistTestsManager(MySqlDBPool *pool)
{
    logger = new Logger();
    dbPool = pool;
}

MySqlNistTestsManager::~MySqlNistTestsManager()
{
    if (logger != nullptr)
        delete logger;
}

bool MySqlNistTestsManager::getParameterById(long id, NistTestParameter &param)
{
    Connection* connection = nullptr;
    PreparedStatement* preparedStmt = nullptr;
    ResultSet *res = nullptr;
    try {
        while((connection = dbPool->getConnectionFromPool()) == nullptr)
            std::this_thread::sleep_for(std::chrono::milliseconds(1));
        preparedStmt = connection->prepareStatement("SELECT id_test, length, test_number, streams, special_parameter FROM nist_tests WHERE id_test=?;");
        preparedStmt->setInt64(1, id);
        res = preparedStmt->executeQuery();
        int i = 0, testNumber;
        long testId, length, streams, specialParameter;
        while (res->next()) {
            testId = res->getInt64("id_test");
            length = res->getInt64("length");
            testNumber = res->getInt("test_number");
            streams = res->getInt64("streams");
            specialParameter = res->getInt64("special_parameter");
            i++;
        }
        if (i == 1) {
            NistTestParameter p(testId,length,testNumber);
            if (streams != 0)
                p.setStreams(streams);
            if (specialParameter != 0)
                p.setSpecialParameter(specialParameter);
            param = p;
        }
        freeResources(connection, preparedStmt, res);
        return (i == 1) ? true : false;
    }catch(exception& ex) {
        logger->logError("getParameterById " + string(ex.what()));
        freeResources(connection, preparedStmt, res);
        return false;
    }
}

void MySqlNistTestsManager::freeResources(Connection* con, PreparedStatement* p, ResultSet* r)
{
    if (p != nullptr)
        delete p;
    if (r != nullptr)
        delete r;
    if (con != nullptr)
        dbPool->releaseConnection(con);
}
