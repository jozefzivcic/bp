#include "mysqlfilemanager.h"
#include "file.h"
#include "mysql_connection.h"
#include "logger.h"
#include <cppconn/driver.h>
#include <cppconn/exception.h>
#include <cppconn/resultset.h>
#include <cppconn/prepared_statement.h>
#include <stdexcept>
#include <mutex>

using namespace std;
using namespace sql;

extern mutex dbMutex;

MySqlFileManager::MySqlFileManager(const ConfigStorage *storage) {
    logger = new Logger();
    dbMutex.lock();
    driver = get_driver_instance();
    dbMutex.unlock();
    driver->threadInit();
    connecion = driver->connect(storage->getDatabase(), storage->getUserName(), storage->getUserPassword());
    connecion->setSchema(storage->getSchema());
}

bool MySqlFileManager::getFileById(int id, File *file) {
    PreparedStatement* preparedStmt = nullptr;
    ResultSet *res = nullptr;
    File tempFile;
    try {
        preparedStmt = connecion->prepareStatement("SELECT id, id_user, hash, name, file_system_path FROM files WHERE id = ?;");
        preparedStmt->setInt(1,id);
        res = preparedStmt->executeQuery();
        int i = 0;
        while (res->next()) {
            tempFile.setId(res->getInt("id"));
            tempFile.setUserId(res->getInt("id_user"));
            tempFile.setHash(res->getString("hash"));
            tempFile.setName(res->getString("name"));
            tempFile.setFileSystemPath(res->getString("file_system_path"));
            i++;
        }
        if (i == 1)
            file->setFile(tempFile);
        deleteStatementAndResSet(preparedStmt,res);
        return (i == 1) ? true : false;
    }catch(exception& ex) {
        logger->logError("getFileById " + string(ex.what()));
        deleteStatementAndResSet(preparedStmt,res);
        return false;
    }
}

MySqlFileManager::~MySqlFileManager() {
    if (connecion != nullptr)
        delete connecion;
    if (logger != nullptr)
        delete logger;
    driver->threadEnd();
}

void MySqlFileManager::deleteStatementAndResSet(PreparedStatement* p, ResultSet* r)
{
    if (p != nullptr)
        delete p;
    if (r != nullptr)
        delete r;
}
