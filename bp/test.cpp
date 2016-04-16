#include "test.h"
#include <iostream>

using namespace std;

Test::Test() : id(0), fileId(0), userId(0), timeOfAdd(0), testTable(""), rerun(false), timeOfRerun(0),
    numOfRuns(0), returnValue(1)
{}

Test::Test(const Test &t) : id(t.getId()), fileId(t.getFileId()), userId(t.getUserId()),
    timeOfAdd(t.getTimeOfAdd()), testTable(t.getTestTable()), rerun(t.getRerun()),
    timeOfRerun(t.getTimeOfRerun()), numOfRuns(t.getNumOfRuns()), returnValue(t.getReturnValue())
{}

long Test::getId() const
{
    return id;
}

void Test::setId(long value)
{
    id = value;
}

long Test::getFileId() const
{
    return fileId;
}

void Test::setFileId(long value)
{
    fileId = value;
}

long Test::getUserId() const
{
    return userId;
}

void Test::setUserId(long value)
{
    userId = value;
}

time_t Test::getTimeOfAdd() const
{
    return timeOfAdd;
}

void Test::setTimeOfAdd(const time_t &value)
{
    timeOfAdd = value;
}

std::string Test::getTestTable() const
{
    return testTable;
}

void Test::setTestTable(const std::string &value)
{
    testTable = value;
}

time_t Test::getTimeOfRerun() const
{
    return timeOfRerun;
}

void Test::setTimeOfRerun(const time_t &value)
{
    timeOfRerun = value;
}

int Test::getNumOfRuns() const
{
    return numOfRuns;
}

void Test::setNumOfRuns(int value)
{
    numOfRuns = value;
}

int Test::getReturnValue() const
{
    return returnValue;
}

void Test::setReturnValue(int value)
{
    returnValue = value;
}

void Test::increaseRuns()
{
    numOfRuns++;
}

bool Test::getRerun() const
{
    return rerun;
}

void Test::setRerun(bool value)
{
    rerun = value;
}

Test& Test::operator =(Test other)
{
    swap(other);
    return *this;
}

ostream& operator <<(ostream &out, const Test &t)
{
    out << "[" << t.id << ", " << t.fileId << ", " << t.userId << ", " << t.timeOfAdd << ", " << t.testTable << "]";
    return out;
}

void Test::swap(Test &t)
{
    using std::swap;
    swap(id, t.id);
    swap(fileId, t.fileId);
    swap(userId, t.userId);
    swap(timeOfAdd, t.timeOfAdd);
    swap(testTable, t.testTable);
    swap(rerun, t.rerun);
    swap(timeOfRerun, t.timeOfRerun);
    swap(numOfRuns, t.numOfRuns);
    swap(returnValue, t.returnValue);
}
