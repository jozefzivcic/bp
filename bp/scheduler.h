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
#include "configstorage.h"
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
    const ConfigStorage* storage;
public:
    friend void interruptHandler(int sig);
    Scheduler(IPriorityComparator * pri, const ConfigStorage* stor);
    ~Scheduler();
    virtual bool getTestForRunning(Test& t) override;
    virtual bool addTestsReadyForRunning() override;
    virtual void run() override;
    virtual bool isStateChanged() override;
};

#endif // SCHEDULER_H
