#include "testhandler.h"
using namespace std;

TestHandler::TestHandler(int num) : maxNumberOfTests(num), numberOfRunningTests(0), endThreads(false)
{
    for(int i = 0; i < num; i++) {
        threads.push_back(thread(threadFunction,this));
    }
}

TestHandler::~TestHandler()
{
    endThreads = true;
    for(int i = 0; i < maxNumberOfTests; i++) {
        threads[i].join();
    }
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


void threadFunction(TestHandler* handler)
{

}
