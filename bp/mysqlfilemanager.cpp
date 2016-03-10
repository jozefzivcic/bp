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

MySqlFileManager::MySqlFileManager(MySqlDBPool *pool) {
    logger = new Logger();
    dbPool = pool;
}

bool MySqlFileManager::getFileById(long id, File *file) {
    Connection* connection = nullptr;
    PreparedStatement* preparedStmt = nullptr;
    ResultSet *res = nullptr;
    File tempFile;
    try {
        connection = dbPool->getConnectionFromPoolBusy();
        preparedStmt = connection->prepareStatement("SELECT id, id_user, hash, name, file_system_path FROM files WHERE id = ?;");
        preparedStmt->setInt64(1,id);
        res = preparedStmt->executeQuery();
        int i = 0;
        while (res->next()) {
            tempFile.setId(res->getInt64("id"));
            tempFile.setUserId(res->getInt64("id_user"));
            tempFile.setHash(res->getString("hash"));
            tempFile.setName(res->getString("name"));
            tempFile.setFileSystemPath(res->getString("file_system_path"));
            i++;
        }
        if (i == 1)
            file->setFile(tempFile);
        freeResources(connection, preparedStmt,res);
        return (i == 1) ? true : false;
    }catch(exception& ex) {
        logger->logError("getFileById " + string(ex.what()));
        freeResources(connection, preparedStmt,res);
        return false;
    }
}

MySqlFileManager::~MySqlFileManager() {
    if (logger != nullptr)
        delete logger;
}

void MySqlFileManager::freeResources(Connection* con, PreparedStatement* p, ResultSet* r)
{
    if (con != nullptr)
        dbPool->releaseConnection(con);
    if (p != nullptr)
        delete p;
    if (r != nullptr)
        delete r;
}
