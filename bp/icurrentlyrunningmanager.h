#ifndef ICURRENTLYRUNNINGMANAGER
#define ICURRENTLYRUNNINGMANAGER
#include "test.h"
class ICurrentlyRunningManager {
public:
    virtual bool insertTest(Test t) = 0;
    virtual bool removeTest(Test t) = 0;
    virtual ~ICurrentlyRunningManager() {}
};

#endif // ICURRENTLYRUNNINGMANAGER

