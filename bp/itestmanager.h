#ifndef ITESTMANAGER
#define ITESTMANAGER
#include "test.h"
#include <list>
class ITestManager {
public:
    virtual std::list<Test> getAllTestsReadyForRunning() = 0;
    virtual ~ITestManager() {}
};

#endif // ITESTMANAGER

