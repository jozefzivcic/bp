#include "scheduler.h"
#include <stdexcept>
#include <list>

using namespace std;

Scheduler::Scheduler(IPriorityComparator *pri) : currentlyRunningProcesses(0), queue(pri), state(0)
{
    numberOfProcessors = std::thread::hardware_concurrency();
    if (numberOfProcessors == 0) {
        throw runtime_error("hardware_concurrency: number of processors = 0");
    }
    maxProcessesRunningParallel = numberOfProcessors + 2;
    testManager = new MySqlTestManager();
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
    while(1) {
        if (queue.size() <= maxProcessesRunningParallel + numberOfProcessors) {

        }
        sleep(1);
    }
}

bool Scheduler::isStateChanged()
{

}

