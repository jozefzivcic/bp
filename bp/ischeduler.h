#ifndef ISCHEDULER
#define ISCHEDULER
#include "test.h"

class IScheduler {
public:
    virtual bool getTestForRunning(Test& t) = 0;
    virtual bool addTestsReadyForRunning() = 0;
    virtual ~IScheduler() {}
};

#endif // ISCHEDULER

