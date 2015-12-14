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

}

Test Scheduler::getTestForRunning()
{
    Test t1, t2, t3;
    t1.setTimeOfAdd(12);
    t2.setTimeOfAdd(13);
    t3.setTimeOfAdd(10);
    queue.push(t2);
    queue.push(t1);
    queue.push(t3);
    cout << queue.top().timeOfAdd() << endl;
    queue.pop();
    cout << queue.top().timeOfAdd() << endl;
    queue.pop();
    cout << queue.top().timeOfAdd() << endl;
    queue.pop();
    return Test();
}

bool Scheduler::addTestsReadyForRunning()
{
    return true;
}

