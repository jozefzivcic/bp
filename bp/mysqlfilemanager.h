#ifndef MYSQLFILEMANAGER
#define MYSQLFILEMANAGER
#include "ifilemanager.h"
#include "configstorage.h"
#include "ilogger.h"
#include "mysqldbpool.h"
#include <mysql_connection.h>
#include <cppconn/driver.h>
#include <cppconn/resultset.h>
#include <cppconn/prepared_statement.h>

/**
 * @brief The MySqlFileManager class implements interface IFileManager. For methods
 * documentation see the interface.
 */
class MySqlFileManager : public IFileManager {
private:
    ILogger* logger = nullptr;
    MySqlDBPool* dbPool = nullptr;
public:
    MySqlFileManager(MySqlDBPool* pool);
    bool getFileById(long id, File* file) override;
    ~MySqlFileManager();
private:

    /**
     * @brief freeResources If con is not nullptr, then this method returns it into pool
     * and if PreparedStatement or ResultSet is not nullptr, then frees them.
     * @param con Connection to be returned to pool.
     * @param p PreparedStatement to be freed.
     * @param r ResultSet to be freed.
     */
    void freeResources(sql::Connection* con, sql::PreparedStatement* p, sql::ResultSet* r);
};

#endif // MYSQLFILEMANAGER

