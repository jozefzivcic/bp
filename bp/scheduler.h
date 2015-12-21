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
#include "ichangestatemanager.h"
#include "mysqlchangestatemanager.h"

class Scheduler : public IScheduler
{
private:
    unsigned int numberOfProcessors;
    unsigned int maxProcessesRunningParallel;
    unsigned int currentlyRunningProcesses;
    std::priority_queue<Test, std::vector<Test>, QueueComparator> queue;
    ITestManager* testManager;
    IChangeStateManager* stateManager;
    int state;
public:
    Scheduler(IPriorityComparator * pri);
    ~Scheduler();
    virtual bool getTestForRunning(Test& t) override;
    virtual bool addTestsReadyForRunning() override;
    virtual void run() override;
    virtual bool isStateChanged() override;
};

#endif // SCHEDULER_H
