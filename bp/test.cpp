#include "test.h"

int Test::id() const
{
    return _id;
}

void Test::setId(int id)
{
    _id = id;
}

int Test::idFile() const
{
    return _idFile;
}

void Test::setIdFile(int idFile)
{
    _idFile = idFile;
}

int Test::idUser() const
{
    return _idUser;
}

void Test::setIdUser(int idUser)
{
    _idUser = idUser;
}

time_t Test::timeOfAdd() const
{
    return _timeOfAdd;
}

void Test::setTimeOfAdd(const time_t &timeOfAdd)
{
    _timeOfAdd = timeOfAdd;
}

std::string Test::testTable() const
{
    return _testTable;
}

void Test::setTestTable(const std::string &testTable)
{
    _testTable = testTable;
}

Test::Test()
{

}

