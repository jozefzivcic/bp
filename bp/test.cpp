#include "test.h"
#include <iostream>

using namespace std;

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

Test& Test::operator =(Test other)
{
    swap(other);
    return *this;
}

ostream& operator <<(ostream &out, const Test &t)
{
    out << "[" << t.id() << ", " << t.idFile() << ", " << t.idUser() << ", " << t.timeOfAdd() << ", " << t.testTable() << "]";
    return out;
}

void Test::swap(Test &t)
{
    using std::swap;
    swap(_id, t._id);
    swap(_idFile, t._idFile);
    swap(_idUser, t._idUser);
    swap(_timeOfAdd, t._timeOfAdd);
    swap(_testTable, t._testTable);
}

Test::Test() : _id(0), _idFile(0), _idUser(0), _timeOfAdd(0), _testTable("")
{}

Test::Test(const Test &t) : _id(t.id()), _idFile(t.idFile()), _idUser(t.idUser()), _timeOfAdd(t.timeOfAdd()), _testTable(t.testTable())
{}

