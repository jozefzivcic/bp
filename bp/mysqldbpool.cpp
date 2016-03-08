#include "mysqldbpool.h"

using namespace std;
using namespace sql;

MySqlDBPool::MySqlDBPool(string db, string usr, string passwd) :
    database(db), user(usr), password(passwd)
{}

Connection *MySqlDBPool::createConnection()
{

}

bool MySqlDBPool::deleteConnection(sql::Connection *con)
{

}

