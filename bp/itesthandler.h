#ifndef ITESTHANDLER
#define ITESTHANDLER
#include "test.h"
class ITestHandler {
public:
    virtual bool createTest(Test t) = 0;
    virtual unsigned int getNumberOfRunningTests() = 0;
};

#endif // ITESTHANDLER

