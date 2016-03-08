#ifndef TESTHANDLER_H
#define TESTHANDLER_H
#include <mutex>
#include <thread>
#include <vector>
#include <condition_variable>
#include "itesthandler.h"
#include "test.h"
#include "threadhandler.h"
#include "configstorage.h"
#include "icurrentlyrunningmanager.h"
#include "ilogger.h"
class TestHandler;

/**
 * @brief threadFunction This is function that is executed by each thread.
 * @param handler Pointer to TestHandler to access its attributes.
 * @param i Serial number of thread.
 */
void threadFunction(TestHandler* handler, int i);

/**
 * @brief The TestHandler class implements interface ITestHandler.
 */
class TestHandler : public ITestHandler
{
private:
    unsigned int maxNumberOfTests;
    unsigned int numberOfRunningTests;
    std::mutex numberOfRunningTestsMutex;
    std::vector<std::thread> threads;
    std::mutex* mutexes = nullptr;
    std::condition_variable* vars = nullptr;
    ThreadHandler* thHandler = nullptr;
    const ConfigStorage* storage;
    ICurrentlyRunningManager* crManager = nullptr;
    ILogger* log = nullptr;
    volatile int signalFromThread;
    std::mutex signalFromThreadMutex;
public:
    friend void threadFunction(TestHandler* handler, int i);

    /**
     * @brief TestHandler Constructor.
     * @param num Maximum number of running tests at same time.
     * @param stor ConfigStorage.
     */
    TestHandler(int num, const ConfigStorage* stor);
    virtual ~TestHandler();
    virtual bool createTest(Test t) override;
    virtual unsigned int getNumberOfRunningTests() override;
private:

    /**
     * @brief addOneTest Adds one test to number of currently running tests.
     */
    void addOneTest();

    /**
     * @brief subtractOneTest Subracts one test to number of currently running tests.
     */
    void subtractOneTest();

    /**
     * @brief setSignal Sets signal to sig.
     * @param sig Value, that is assigned to signal.
     */
    void setSignal(int sig);

    /**
     * @brief getSignal Gets current signal.
     * @return Current signal value.
     */
    int getSignal();
};

#endif // TESTHANDLER_H
