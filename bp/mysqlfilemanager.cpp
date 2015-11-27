#include "mysqlfilemanager.h"
#include "file.h"
#include "mysql_connection.h"
#include <cppconn/driver.h>
#include <cppconn/exception.h>
#include <cppconn/resultset.h>
#include <cppconn/prepared_statement.h>
#include "constants.h"
#include <stdexcept>
using namespace std;
using namespace sql;

MySqlFileManager::MySqlFileManager() {
    Driver *driver;
    driver = get_driver_instance();
    _con = driver->connect(Constants::DATABASE, Constants::USERNAME, Constants::USER_PASSWORD);
    _con->setSchema(Constants::SCHEMA);
}

bool MySqlFileManager::getFileById(int id, File *file) const {
    PreparedStatement* preparedStmt;
    ResultSet *res;
    File tempFile;
    try {
        preparedStmt = _con->prepareStatement("SELECT id, id_user, hash, name, file_system_path FROM files WHERE id = ? ;");
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
        delete res;
        delete preparedStmt;
        return (i == 1) ? true : false;
    }catch(exception) {
        delete res;
        delete preparedStmt;
        return false;
    }
}

MySqlFileManager::~MySqlFileManager() {
    delete _con;
}
