#include "scheduler.h"
#include <stdexcept>

using namespace std;

Scheduler::Scheduler(IPriorityComparator *pri) : currentlyRunningProcesses(0), queue(pri)
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
    return true;
}

