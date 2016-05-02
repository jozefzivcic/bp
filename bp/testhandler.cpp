#include "testhandler.h"
#include "itestcreator.h"
#include "testcreator.h"
#include "mysqlcurrentlyrunningmanager.h"
#include "itestmanager.h"
#include "mysqltestmanager.h"
#include "ifilestructurehandler.h"
#include "linuxfilestructurehandler.h"
#include "logger.h"
#include <sys/types.h>
#include <sys/wait.h>
#include <sched.h>
#include <cppconn/driver.h>
#include <sys/types.h>
#include <signal.h>

using namespace std;

TestHandler::TestHandler(int num, const ConfigStorage *stor, MySqlDBPool *pool):
    maxNumberOfTests(num), numberOfRunningTests(0), storage(stor)
{
    dbPool = pool;
    mutexes = new mutex[num];
    vars = new condition_variable[num];
    thHandler = new ThreadHandler(num);
    crManager = new MySqlCurrentlyRunningManager(pool);
    log = new Logger();
    for(int i = 0; i < num; i++) {
        threads.push_back(thread(threadFunction, this, i));
    }
}

TestHandler::~TestHandler()
{
    thHandler->stopAllThreads();
    for (unsigned int i = 0; i < maxNumberOfTests; i++) {
        vars[i].notify_one();
    }
    for(unsigned int i = 0; i < maxNumberOfTests; i++) {
        threads[i].join();
    }
    delete[] mutexes;
    delete[] vars;
    if (crManager != nullptr)
        delete crManager;
    if (thHandler != nullptr)
        delete thHandler;
    if (log != nullptr)
        delete log;
}

bool TestHandler::createTest(Test t)
{
    if (getNumberOfRunningTests() >= maxNumberOfTests)
        return false;
    int index = thHandler->getIndexOfFreeThread();
    if (index == -1)
       return false;
    addOneTest();
    thHandler->setTestAtPosition(index, t);
    thHandler->setThreadAtPositionIsBusy(index);
    crManager->insertTest(t);
    setSignal(-1);
    vars[index].notify_one();
    int i = 0;
    while(i < 10 && getSignal() == -1) {
        this_thread::sleep_for(chrono::milliseconds(1));
        i++;
    }
    return i != 10;
}

unsigned int TestHandler::getNumberOfRunningTests()
{
    int num;
    numberOfRunningTestsMutex.lock();
    num = numberOfRunningTests;
    numberOfRunningTestsMutex.unlock();
    return num;
}

void TestHandler::addOneTest()
{
    numberOfRunningTestsMutex.lock();
    numberOfRunningTests += 1;
    numberOfRunningTestsMutex.unlock();
}

void TestHandler::subtractOneTest()
{
    numberOfRunningTestsMutex.lock();
    bool send = false;
    if (numberOfRunningTests == maxNumberOfTests)
        send = true;
    numberOfRunningTests -= 1;
    if (send)
        kill(getpid(), SIGUSR1);
    numberOfRunningTestsMutex.unlock();
}

void TestHandler::setSignal(int sig)
{
    signalFromThreadMutex.lock();
    signalFromThread = sig;
    signalFromThreadMutex.unlock();
}

int TestHandler::getSignal()
{
    int temp;
    signalFromThreadMutex.lock();
    temp = signalFromThread;
    signalFromThreadMutex.unlock();
    return temp;
}

void threadFunction(TestHandler* handler, int i)
{
    unique_lock<mutex>lck(handler->mutexes[i]);
    ITestCreator* testCreator = new TestCreator(handler->storage, handler->dbPool);
    ICurrentlyRunningManager* crManager = new MySqlCurrentlyRunningManager(handler->dbPool);
    IFileStructureHandler* fileHandler = new LinuxFileStructureHandler(handler->storage);
    ILogger* logger = new Logger();
    list<string> l;
    l.push_back(handler->storage->getPathToTestsPool());
    l.push_back(to_string(i));
    string bin = fileHandler->createFSPath(true, l);
    unshare(CLONE_FS);
    if (chdir(bin.c_str()) != 0)
        throw runtime_error("chdir");
    handler->thHandler->setThreadAtPositionIsReady(i);
    while(!(handler->thHandler)->shouldThreadStop()) {
        handler->vars[i].wait(lck);
        handler->setSignal(i);
        if (handler->thHandler->shouldThreadStop())
            break;
        Test myTest;
        handler->thHandler->getTestAtPosition(i, myTest);
        logger->logInfo("test " + to_string(myTest.getId()) + " started in thread " + to_string(i));
        testCreator->createTest(myTest);
        logger->logInfo("test " + to_string(myTest.getId()) + " finished in thread " + to_string(i));
        crManager->removeTest(myTest);
        handler->subtractOneTest();
        handler->thHandler->setThreadAtPositionIsReady(i);
    }
    logger->logInfo("Thread " + to_string(i) + " ended");
    delete fileHandler;
    delete testCreator;
    delete crManager;
    delete logger;
}
