#include "testhandler.h"

TestHandler::TestHandler() : numberOfRunningTests(0)
{

}

bool TestHandler::createNistTest(Test t)
{

}

int TestHandler::getNumberOfRunningTests()
{
    int num;
    numberOfRunningTestsMutex.lock();
    num = numberOfRunningTests;
    numberOfRunningTestsMutex.unlock();
    return num;
}

void TestHandler::addOneTest()
{
    numberOfRunningTestsMutex.lock();
    numberOfRunningTests += 1;
    numberOfRunningTestsMutex.unlock();
}

void TestHandler::subtractOneTest()
{
    numberOfRunningTestsMutex.lock();
    numberOfRunningTests -= 1;
    numberOfRunningTestsMutex.unlock();
}

