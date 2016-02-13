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
#include "itesthandler.h"

class Scheduler : public IScheduler
{
private:
    std::priority_queue<Test, std::vector<Test>, QueueComparator> queue;
    int state;
    const ConfigStorage* storage;
    unsigned int maxTestsRunningParallel;
    ITestManager* testManager = nullptr;
    IChangeStateManager* stateManager = nullptr;
    ITestHandler* testHandler = nullptr;
public:
    Scheduler(IPriorityComparator * pri, const ConfigStorage* stor, int maxParallel);
    ~Scheduler();
    virtual bool getTestForRunning(Test& t) override;
    virtual bool addTestsReadyForRunning() override;
    virtual void run() override;
    virtual bool isStateChanged() override;
};

#endif // SCHEDULER_H
