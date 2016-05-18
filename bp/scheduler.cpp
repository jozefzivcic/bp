#include "scheduler.h"
#include <stdexcept>
#include <list>
#include "testhandler.h"
#include "logger.h"
#include "mysqlpidtablemanager.h"
#include <sys/types.h>
#include <unistd.h>

using namespace std;

extern bool endProgram;

Scheduler::Scheduler(IPriorityComparator *pri, const ConfigStorage* stor, int maxParallel)
    : queue(pri), storage(stor), maxTestsRunningParallel(maxParallel)
{
    dbPool = new MySqlDBPool(stor->getDatabase(), stor->getUserName(), stor->getUserPassword(),
                             stor->getSchema());
    if (!dbPool->createPool(stor->getPooledConnections()))
        throw runtime_error("Scheduler::Scheduler::createPool");
    testManager = new MySqlTestManager(dbPool);
    testHandler = new TestHandler(maxParallel, stor, dbPool);
    sleepInSeconds = stor->getSleepInSeconds();
    logger = new Logger();
    pidManager = new MySqlPIDTableManager(dbPool);
    if (!storePID())
        throw runtime_error("Scheduler::Scheduler::storePID()");
}

Scheduler::~Scheduler()
{
    removePID();
    if (testManager != nullptr)
        delete testManager;
    if (testHandler != nullptr)
        delete testHandler;
    if (pidManager != nullptr)
        delete pidManager;
    if (dbPool != nullptr) {
        dbPool->destroyPool();
        delete dbPool;
    }
    if (logger != nullptr)
        delete logger;
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
    list<Test> l;
    if (!testManager->getAllTestsReadyForRunning(l))
        return false;
    for (Test t : l) {
        if (t.getRerun()) {
            if (!testManager->setTestAsLoadedForRerun(t))
                return false;
        }
        else {
            if (!testManager->setTestAsLoaded(t))
                return false;
        }
        queue.push(t);
    }
    return true;
}

void Scheduler::run()
{
    while(!endProgram) {
        if ((queue.size() <= maxTestsRunningParallel * 2))
            addTestsReadyForRunning();
        while(!queue.empty() && testHandler->getNumberOfRunningTests() < maxTestsRunningParallel) {
            Test t;
            getTestForRunning(t);
            if (!testHandler->createTest(t)) {
                logger->logWarning("Test was not created and is pushed back to queue " + to_string(t.getId()));
                queue.push(t);
            }
        }
        sleep(sleepInSeconds);
    }
}

bool Scheduler::addTestsAfterCrash()
{
    list<Test> l;
    if (!testManager->getTestsNotFinished(l))
        return false;
    for (Test t : l) {
        queue.push(t);
    }
    return true;
}

bool Scheduler::storePID()
{
    pid_t this_process = getpid();
    return pidManager->storePIDForId(storage->getIdOfPid(), this_process);
}

bool Scheduler::removePID()
{
    return pidManager->removePIDForId(storage->getIdOfPid());
}
