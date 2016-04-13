#include "scheduler.h"
#include <stdexcept>
#include <list>
#include "ichangestatemanager.h"
#include "mysqlchangestatemanager.h"
#include "testhandler.h"

using namespace std;

extern bool endProgram;

Scheduler::Scheduler(IPriorityComparator *pri, const ConfigStorage* stor, int maxParallel)
    : queue(pri), state(-1), storage(stor), maxTestsRunningParallel(maxParallel)
{
    dbPool = new MySqlDBPool(stor->getDatabase(), stor->getUserName(), stor->getUserPassword(),
                             stor->getSchema());
    dbPool->createPool(stor->getPooledConnections());
    testManager = new MySqlTestManager(dbPool);
    stateManager = new MySqlChangeStateManager(dbPool);
    testHandler = new TestHandler(maxParallel, stor, dbPool);
    sleepInSeconds = stor->getSleepInSeconds();
}

Scheduler::~Scheduler()
{
    if (testManager != nullptr)
        delete testManager;
    if (stateManager != nullptr)
        delete stateManager;
    if (testHandler != nullptr)
        delete testHandler;
    if (dbPool != nullptr) {
        dbPool->destroyPool();
        delete dbPool;
    }
}

bool Scheduler::getTestForRunning(Test &t)
{
    if (!queue.empty()) {
        t = queue.top();
        queue.pop();
        return true;
    }
    return false;
}

bool Scheduler::addTestsReadyForRunning()
{
    list<Test> l;
    if (!testManager->getAllTestsReadyForRunning(l))
        return false;
    for (Test t : l) {
        if (!testManager->setTestAsLoaded(t))
            return false;
        queue.push(t);
    }
    return true;
}

void Scheduler::run()
{
    long tempState = 0;
    while(!endProgram) {
        if ((queue.size() <= maxTestsRunningParallel * 2) && isStateChanged(tempState)) {
            addTestsReadyForRunning();
            state = tempState;
        }
        while(!queue.empty() && testHandler->getNumberOfRunningTests() < maxTestsRunningParallel) {
            Test t;
            getTestForRunning(t);
            if (!testHandler->createTest(t))
                queue.push(t);
        }
        sleep(sleepInSeconds);
    }
}

bool Scheduler::isStateChanged(long& retState)
{
    long dbState = 0L;
    if (!stateManager->getDBState(dbState))
        return true;
    if (dbState == state)
        return false;
    retState = dbState;
    return true;
}

bool Scheduler::addTestsAfterCrash()
{
    list<Test> l;
    if (!testManager->getTestsNotFinished(l))
        return false;
    for (Test t : l) {
        queue.push(t);
    }
    return true;
}
