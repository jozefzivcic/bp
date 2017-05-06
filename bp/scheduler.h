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
 * see the interface.
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

    /**
     * @brief removePIDAtTheEnd Flag that states, if PID can be deleted from database at the end of this program.
     */
    bool removePIDAtTheEnd = false;

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

    /**
     * @brief checkIfProcessExists Checks if process with pid exists in the system.
     * @param pid PID of process, which is cotrolled for running.
     * @return True if process with such PID exists, false otherwise.
     */
    bool checkIfProcessExists(pid_t pid);

    /**
     * @brief controllPIDInDatabase Controlls if database contains any record in table pid_table with id,
     * that is stored under key SCHEDULER_ID_OF_PID. If table contains any record and process with this PID is running,
     * then do nothing. Else removes record with this PID and stores new PID for this program.
     * @return True if program can continue, false if can't.
     */
    bool controllPIDInDatabase();
};

#endif // SCHEDULER_H
