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
    con = driver->connect(Constants::DATABASE, Constants::USERNAME, Constants::USER_PASSWORD);
    con->setSchema(Constants::SCHEMA);
}

File MySqlFileManager::getFileById(int id) const {
    PreparedStatement* preparedStmt;
    ResultSet *res;
    File f;
    try {
        preparedStmt = con->prepareStatement("SELECT id, id_user, hash, name, file_system_path FROM files WHERE id = ? ;");
        preparedStmt->setInt(1,id);
        res = preparedStmt->executeQuery();
        res->next();
        cout << res->getInt("id");
        f.setId(res->getInt("id"));
        f.setUserId(res->getInt("id_user"));
        f.setHash(res->getString("hash"));
        f.setName(res->getString("name"));
        f.setFileSystemPath(res->getString("file_system_path"));
        delete res;
        delete preparedStmt;
        return f;
    }catch(InvalidArgumentException) {
        delete res;
        delete preparedStmt;
        return f;
    }
}

MySqlFileManager::~MySqlFileManager() {
    delete con;
}
