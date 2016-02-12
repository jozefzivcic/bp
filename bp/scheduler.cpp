#include "scheduler.h"
#include <stdexcept>
#include <list>
#include "ichangestatemanager.h"
#include "mysqlchangestatemanager.h"

using namespace std;
extern bool endProgram;
Scheduler::Scheduler(IPriorityComparator *pri, const ConfigStorage* stor)
    : currentlyRunningProcesses(0), queue(pri), state(0), storage(stor)
{
    numberOfProcessors = thread::hardware_concurrency();
    if (numberOfProcessors == 0) {
        throw runtime_error("hardware_concurrency: number of processors = 0");
    }
    maxProcessesRunningParallel = numberOfProcessors + 2;
    testManager = new MySqlTestManager(stor);
    stateManager = new MySqlChangeStateManager(stor);
}

Scheduler::~Scheduler()
{
    if (testManager != nullptr)
        delete testManager;

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
        /*if ((queue.size() <= maxProcessesRunningParallel + numberOfProcessors) && isStateChanged()) {
            addTestsReadyForRunning();
        }*/
        sleep(1);
    }
    cout << endProgram << endl;
}

bool Scheduler::isStateChanged()
{
    int dbState;
    stateManager->getDBState(dbState);
    if (dbState != state)
        return false;
    state = dbState;
    return true;
}

