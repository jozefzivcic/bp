#include "testhandler.h"
#include "itestcreator.h"
#include "testcreator.h"
#include "icurrentlyrunningmanager.h"
#include "mysqlcurrentlyrunningmanager.h"

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
    thHandler.stopAllThreads();
    for (int i = 0; i < maxNumberOfTests; i++) {
        vars[i].notify_one();
    }
    for(int i = 0; i < maxNumberOfTests; i++) {
        threads[i].join();
    }
    delete[] mutexes;
    delete[] vars;
}

bool TestHandler::createTest(Test t)
{
    if (getNumberOfRunningTests() >= maxNumberOfTests)
        return false;
    int index = thHandler.getIndexOfFreeThread();
    if (index == -1)
       return false;
    addOneTest();
    thHandler.setTestAtPosition(index,t);
    thHandler.setThreadAtPositionIsBusy(index);
    ICurrentlyRunningManager* manager = new MySqlCurrentlyRunningManager();
    manager->insertTest(t);
    delete manager;
    vars[index].notify_one();
    return true;
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
    ICurrentlyRunningManager* manager = new MySqlCurrentlyRunningManager();
    while(handler->thHandler.shouldThreadStopped()) {
        handler->vars[i].wait(lck);
        if (handler->thHandler.shouldThreadStopped())
            break;
        Test myTest;
        handler->thHandler.getTestAtPosition(i,myTest);
        testCreator->createTest(myTest);
        manager->removeTest(myTest);
        handler->subtractOneTest();
        handler->thHandler.setThreadAtPositionIsReady(i);
    }
    delete testCreator;
    delete manager;
}
