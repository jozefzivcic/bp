#include "testhandler.h"
#include "itestcreator.h"
#include "testcreator.h"
#include "mysqlcurrentlyrunningmanager.h"
#include "itestmanager.h"
#include "mysqltestmanager.h"

using namespace std;

TestHandler::TestHandler(int num, const ConfigStorage *stor):
    maxNumberOfTests(num), numberOfRunningTests(0), storage(stor)
{
    mutexes = new mutex[num];
    vars = new condition_variable[num];
    thHandler = new ThreadHandler(num);
    crManager = new MySqlCurrentlyRunningManager(stor);
    for(int i = 0; i < num; i++) {
        threads.push_back(thread(threadFunction,this,i));
    }
}

TestHandler::~TestHandler()
{
    thHandler->stopAllThreads();
    for (unsigned int i = 0; i < maxNumberOfTests; i++) {
        vars[i].notify_one();
    }
    for(unsigned int i = 0; i < maxNumberOfTests; i++) {
        threads[i].join();
    }
    delete[] mutexes;
    delete[] vars;
    if (crManager != nullptr)
        delete crManager;
    if (thHandler != nullptr)
        delete thHandler;
}

bool TestHandler::createTest(Test t)
{
    if (getNumberOfRunningTests() >= maxNumberOfTests)
        return false;
    int index = thHandler->getIndexOfFreeThread();
    if (index == -1)
       return false;
    addOneTest();
    thHandler->setTestAtPosition(index,t);
    thHandler->setThreadAtPositionIsBusy(index);
    crManager->insertTest(t);
    vars[index].notify_one();
    return true;
}

unsigned int TestHandler::getNumberOfRunningTests()
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
    ITestCreator* testCreator = new TestCreator(handler->storage);
    ITestManager* testManager = new MySqlTestManager(handler->storage);
    ICurrentlyRunningManager* crManager = new MySqlCurrentlyRunningManager(handler->storage);

    while(handler->thHandler->shouldThreadStopped()) {
        handler->vars[i].wait(lck);
        if (handler->thHandler->shouldThreadStopped())
            break;
        Test myTest;
        handler->thHandler->getTestAtPosition(i, myTest);
        testCreator->createTest(i, myTest);
        testManager->setTestHasFinished(myTest);
        crManager->removeTest(myTest);
        handler->thHandler->setThreadAtPositionIsReady(i);
        handler->subtractOneTest();
    }
    delete testCreator;
    delete testManager;
    delete crManager;
}
