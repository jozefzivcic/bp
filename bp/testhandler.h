#ifndef TESTHANDLER_H
#define TESTHANDLER_H
#include <mutex>
#include <thread>
#include <vector>
#include <condition_variable>
#include "itesthandler.h"
#include "test.h"
#
class TestHandler;
void threadFunction(TestHandler* handler);

class TestHandler : public ITestHandler
{
private:
    int maxNumberOfTests;
    int numberOfRunningTests;
    std::mutex numberOfRunningTestsMutex;
    Test test;
    bool endThreads;
    std::vector<std::thread> threads;
    std::condition_variable var;
public:
    TestHandler(int num);
    virtual ~TestHandler();
    virtual bool createNistTest(Test t) override;
    virtual int getNumberOfRunningTests() override;
private:
    void addOneTest();
    void subtractOneTest();
};

#endif // TESTHANDLER_H
