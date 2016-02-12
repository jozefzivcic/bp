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

class TestHandler;
void threadFunction(TestHandler* handler, int i);

class TestHandler : public ITestHandler
{
private:
    int maxNumberOfTests;
    int numberOfRunningTests;
    std::mutex numberOfRunningTestsMutex;
    std::vector<std::thread> threads;
    std::mutex* mutexes;
    std::condition_variable* vars;
    ThreadHandler thHandler;
    const ConfigStorage* storage;
public:
    friend void threadFunction(TestHandler* handler, int i);
    TestHandler(int num, const ConfigStorage* stor);
    virtual ~TestHandler();
    virtual bool createTest(Test t) override;
    virtual int getNumberOfRunningTests() override;
private:
    void addOneTest();
    void subtractOneTest();
};

#endif // TESTHANDLER_H
