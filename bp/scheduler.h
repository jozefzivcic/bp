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
#include "configstorage.h"
#include "itesthandler.h"
#include "mysqldbpool.h"
#include "ilogger.h"
#include "ipidtablemanager.h"
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
     * @brief storage ConfigStorage.
     */
    const ConfigStorage* storage;

    /**
     * @brief maxTestsRunningParallel Maximum number of tests that can run in parallel.
     */
    unsigned int maxTestsRunningParallel;

    ITestManager* testManager = nullptr;
    ITestHandler* testHandler = nullptr;
    MySqlDBPool* dbPool = nullptr;
    size_t sleepInSeconds;
    ILogger* logger = nullptr;
    IPIDTableManager* pidManager = nullptr;
public:
    Scheduler(IPriorityComparator * pri, const ConfigStorage* stor, int maxParallel);
    ~Scheduler();
    virtual bool getTestForRunning(Test& t) override;
    virtual bool addTestsReadyForRunning() override;
    virtual void run() override;
    virtual bool addTestsAfterCrash() override;
private:

    /**
     * @brief storePID Stores pid of this process to the database.
     * @return If an error occurs false, true otherwise.
     */
    bool storePID();

    /**
     * @brief removePID Removes pid of this process from the database.
     * @return If an error occurs false, true otherwise.
     */
    bool removePID();
};

#endif // SCHEDULER_H
