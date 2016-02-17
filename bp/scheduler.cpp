#include "scheduler.h"
#include <stdexcept>
#include <list>
#include "ichangestatemanager.h"
#include "mysqlchangestatemanager.h"
#include "testhandler.h"

using namespace std;

extern bool endProgram;

Scheduler::Scheduler(IPriorityComparator *pri, const ConfigStorage* stor, int maxParallel)
    : queue(pri), state(0), storage(stor), maxTestsRunningParallel(maxParallel)
{
    testManager = new MySqlTestManager(stor);
    stateManager = new MySqlChangeStateManager(stor);
    testHandler = new TestHandler(maxParallel, stor);
}

Scheduler::~Scheduler()
{
    if (testManager != nullptr)
        delete testManager;
    if (stateManager != nullptr)
        delete stateManager;
    if (testHandler != nullptr)
        delete testHandler;
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
        queue.push(t);
    }
    return true;
}

void Scheduler::run()
{
    while(!endProgram) {
        if ((queue.size() <= maxTestsRunningParallel * 2) && isStateChanged()) {
            addTestsReadyForRunning();
        }
        while(!queue.empty() && testHandler->getNumberOfRunningTests() < maxTestsRunningParallel) {
            Test t;
            getTestForRunning(t);
            if (!testHandler->createTest(t))
                queue.push(t);
        }
        sleep(1);
    }
    cout << endProgram << endl;
}

bool Scheduler::isStateChanged()
{
    int dbState;
    stateManager->getDBState(dbState);
    if (dbState == state)
        return false;
    state = dbState;
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
