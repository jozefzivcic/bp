#ifndef SCHEDULER_H
#define SCHEDULER_H
#include <thread>
#include <map>
#include <queue>
#include <list>
#include "ischeduler.h"
#include "queuecomparator.h"
#include "prioritycomparator.h"

class Scheduler : public IScheduler
{
private:
    int numberOfProcessors;
    int maxProcessesRunningParallel;
    int currentlyRunningProcesses;
    std::priority_queue<Test, std::vector<Test>, QueueComparator> queue;
public:
    Scheduler(IPriorityComparator * pri);
    ~Scheduler(){}
    virtual Test getTestForRunning() override;
    virtual bool addTestsReadyForRunning() override;
};

#endif // SCHEDULER_H
