#ifndef MYSQLFILEMANAGER
#define MYSQLFILEMANAGER
#include "ifilemanager.h"
#include "configstorage.h"
#include "ilogger.h"
#include <mysql_connection.h>
#include <cppconn/driver.h>
#include <cppconn/resultset.h>
#include <cppconn/prepared_statement.h>

/**
 * @brief The MySqlFileManager class implements interface IFileManager. For methods
 * documentation see interface.
 */
class MySqlFileManager : public IFileManager {
private:
    sql::Driver *driver;
    sql::Connection* connecion = nullptr;
    ILogger* logger = nullptr;
public:
    MySqlFileManager(const ConfigStorage* storage);
    bool getFileById(int id, File* file) override;
    ~MySqlFileManager();
private:

    /**
     * @brief deleteStatementAndResSet If PreparedStatement or ResultSet is not nullptr,
     * then frees them.
     * @param p PreparedStatement to be freed.
     * @param r ResultSet to be freed.
     */
    void deleteStatementAndResSet(sql::PreparedStatement* p, sql::ResultSet* r);
};

#endif // MYSQLFILEMANAGER

