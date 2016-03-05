#include "mysqlnisttestsmanager.h"
#include "logger.h"
#include <cppconn/driver.h>
#include <mutex>

using namespace std;
using namespace sql;

extern mutex dbMutex;

MySqlNistTestsManager::MySqlNistTestsManager(const ConfigStorage *storage)
{
    logger = new Logger();
    dbMutex.lock();
    driver = get_driver_instance();
    dbMutex.unlock();
    driver->threadInit();
    connection = driver->connect(storage->getDatabase(), storage->getUserName(), storage->getUserPassword());
    connection->setSchema(storage->getSchema());
}

MySqlNistTestsManager::~MySqlNistTestsManager()
{
    if (connection != nullptr)
        delete connection;
    if (logger != nullptr)
        delete logger;
    driver->threadEnd();
}

bool MySqlNistTestsManager::getParameterById(long id, NistTestParameter &param)
{
    PreparedStatement* preparedStmt = nullptr;
    ResultSet *res = nullptr;
    try {
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
        deleteStatementAndResSet(preparedStmt,res);
        return (i == 1) ? true : false;
    }catch(exception& ex) {
        logger->logError("getParameterById " + string(ex.what()));
        deleteStatementAndResSet(preparedStmt,res);
        return false;
    }
}

void MySqlNistTestsManager::deleteStatementAndResSet(PreparedStatement* p, ResultSet* r)
{
    if (p != nullptr)
        delete p;
    if (r != nullptr)
        delete r;
}
