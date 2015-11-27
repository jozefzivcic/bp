#ifndef ITESTMANAGER
#define ITESTMANAGER
#include "test.h"
#include <vector>
class ITestManager {
public:
    virtual std::vector<Test> getAllTestsReadyForRunning() const = 0;
    virtual ~ITestManager() {}
};

#endif // ITESTMANAGER

