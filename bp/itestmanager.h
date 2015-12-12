#ifndef ITESTMANAGER
#define ITESTMANAGER
#include "test.h"
#include <list>
class ITestManager {
public:

    /**
     * @brief getAllTestsReadyForRunning If function succeeds, appends all tests ready for running
     * into parameter t. This tests are sorted by time of add ascending.
     * @param t List of tests, which is filled with tests ready for running.
     * @return If function succeeds and no error occurs, return value is true, false otherwise.
     */
    virtual bool getAllTestsReadyForRunning(std::list<Test>& t) = 0;

    /**
     * @brief setTestHasStarted Sets flags in database, that given test has already started
     * and has not finished yet.
     * @param t Test which is marked as running.
     * @return If given test does not exists, or an error occurs, return value is false, true otherwise.
     */
    virtual bool setTestHasStarted(Test t) = 0;

    /**
     * @brief setTestHasFinished Sets flag in database, that given test has already ended.
     * @param t Test which is marked as finished.
     * @return If given test does not exists, is not running, or an error occurs,
     * return value is false, true otherwise.
     */
    virtual bool setTestHasFinished(Test t) = 0;

    /**
     * @brief ~ITestManager
     */
    virtual ~ITestManager() {}
};

#endif // ITESTMANAGER

