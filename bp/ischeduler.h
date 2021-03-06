#ifndef ISCHEDULER
#define ISCHEDULER
#include "test.h"

/**
 * @brief The IScheduler class fills tests from database, decides, which test to execute
 * and can also re-run tests, which not finished because of program crash.
 */
class IScheduler {
public:

    /**
     * @brief getTestForRunning Sets attributes of parameter t according to test,
     * which will run as next.
     * @param t Test which attributes are set.
     * @return If an error occurs, return value is false and param t is not changed, true otherwise.
     */
    virtual bool getTestForRunning(Test& t) = 0;

    /**
     * @brief addTestsReadyForRunning Adds tests from database into a queue of tests for running.
     * @return If an error occurs false, true otherwise.
     */
    virtual bool addTestsReadyForRunning() = 0;

    /**
     * @brief run Starts scheduler.
     */
    virtual void run() = 0;

    /**
     * @brief addTestsAfterCrash Adds tests to the queue of tests for running after these tests
     * were loaded but not finished.
     * @return If an error occurs false, true otherwise.
     */
    virtual bool addTestsAfterCrash() = 0;

    /**
     * @brief ~IScheduler Virtual destructor.
     */
    virtual ~IScheduler() {}
};

#endif // ISCHEDULER

