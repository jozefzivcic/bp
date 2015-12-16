#ifndef SCHEDULER_H
#define SCHEDULER_H
#include <thread>
#include <map>
#include <queue>
#include <list>
#include "ischeduler.h"
#include "queuecomparator.h"
#include "prioritycomparator.h"
#include "itestmanager.h"
#include "mysqltestmanager.h"

class Scheduler : public IScheduler
{
private:
    int numberOfProcessors;
    int maxProcessesRunningParallel;
    int currentlyRunningProcesses;
    std::priority_queue<Test, std::vector<Test>, QueueComparator> queue;
    ITestManager* testManager;
public:
    Scheduler(IPriorityComparator * pri);
    ~Scheduler();
    virtual bool getTestForRunning(Test& t) override;
    virtual bool addTestsReadyForRunning() override;
};

#endif // SCHEDULER_H
