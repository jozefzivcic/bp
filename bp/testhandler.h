#ifndef TESTHANDLER_H
#define TESTHANDLER_H
#include <mutex>
#include "itesthandler.h"

class TestHandler : public ITestHandler
{
private:
    int numberOfRunningTests;
    std::mutex numberOfRunningTestsMutex;
public:
    TestHandler();
    virtual bool createNistTest(Test t) override;
    virtual int getNumberOfRunningTests() override;
private:
    void addOneTest();
    void subtractOneTest();
};

#endif // TESTHANDLER_H
