#ifndef ITESTHANDLER
#define ITESTHANDLER
#include "test.h"

/**
 * @brief The ITestHandler class creates tests and does not wait for their finish. More than
 * one test can run unter this class at the same time.
 */
class ITestHandler {
public:

    /**
     * @brief createTest Creates test.
     * @param t Test to be created.
     * @return
     */
    virtual bool createTest(Test t) = 0;

    /**
     * @brief getNumberOfRunningTests Gets number of running tests under this class.
     * @return Number of currently running tests.
     */
    virtual unsigned int getNumberOfRunningTests() = 0;

    /**
     * @brief ~ITestHandler Virtual destructor.
     */
    virtual ~ITestHandler() {}
};

#endif // ITESTHANDLER

