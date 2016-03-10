#ifndef MYSQLNISTTESTSMANAGER_H
#define MYSQLNISTTESTSMANAGER_H
#include "inisttestsmanager.h"
#include "configstorage.h"
#include "ilogger.h"
#include "mysqldbpool.h"
#include <mysql_connection.h>
#include <cppconn/resultset.h>
#include <cppconn/prepared_statement.h>

/**
 * @brief The MySqlNistTestsManager class implements interface INistTestsManager. For methods
 * documentation see interface.
 */
class MySqlNistTestsManager : public INistTestsManager
{
private:
    ILogger* logger = nullptr;
    MySqlDBPool* dbPool = nullptr;
public:
    MySqlNistTestsManager(MySqlDBPool* pool);
    ~MySqlNistTestsManager();
    virtual bool getParameterById(long id, NistTestParameter& param) override;
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

#endif // MYSQLNISTTESTSMANAGER_H
