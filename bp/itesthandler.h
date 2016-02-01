#ifndef ITESTHANDLER
#define ITESTHANDLER
#include "test.h"
class ITestHandler {
public:
    virtual bool createNistTest(Test t) = 0;
    virtual int getNumberOfRunningTests() = 0;
};

#endif // ITESTHANDLER

