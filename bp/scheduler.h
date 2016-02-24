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

/**
 * @brief The Scheduler class implements interface IScheduler. For methods documentation
 * see interface.
 */
class Scheduler : public IScheduler
{
private:

    /**
     * @brief queue Priority queue that orders tests according to given QueueComparator.
     */
    std::priority_queue<Test, std::vector<Test>, QueueComparator> queue;

    /**
     * @brief state State of database.
     */
    int state = 0;

    /**
     * @brief storage ConfigStorage.
     */
    const ConfigStorage* storage;

    /**
     * @brief maxTestsRunningParallel Maximum number of tests that can run in parallel.
     */
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
    virtual bool addTestsAfterCrash() override;
};

#endif // SCHEDULER_H
