#include "testhandler.h"
#include "itestcreator.h"
#include "testcreator.h"

using namespace std;

TestHandler::TestHandler(int num) : maxNumberOfTests(num), numberOfRunningTests(0), thHandler(num)
{
    mutexes = new mutex[num];
    vars = new condition_variable[num];
    for(int i = 0; i < num; i++) {
        threads.push_back(thread(threadFunction,this,i));
    }
}

TestHandler::~TestHandler()
{
    for(int i = 0; i < maxNumberOfTests; i++) {
        threads[i].join();
    }
    delete[] mutexes;
    delete[] vars;
}

bool TestHandler::createTest(Test t)
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


void threadFunction(TestHandler* handler, int i)
{
    unique_lock<mutex>lck(handler->mutexes[i]);
    ITestCreator* testCreator = new TestCreator();
    while(handler->thHandler.shouldThreadStopped()) {
        handler->vars[i].wait(lck);
        if (handler->thHandler.shouldThreadStopped())
            break;
        Test myTest;
        handler->thHandler.getTestAtPosition(i,myTest);
        testCreator->createTest(myTest);
        handler->thHandler.setThreadAtPositionIsReady(i);
    }
}
