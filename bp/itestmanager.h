#ifndef ITESTMANAGER
#define ITESTMANAGER
#include "test.h"
#include <list>

/**
 * @brief The ITestManager class manages database table tests.
 */
class ITestManager {
public:

    /**
     * @brief getAllTestsReadyForRunning If function succeeds, appends all tests ready for running
     * into parameter t.
     * @param t List of tests, which is filled with tests ready for running.
     * @return If function succeeds and no error occurs, return value is true, false otherwise.
     */
    virtual bool getAllTestsReadyForRunning(std::list<Test>& t) = 0;

    /**
     * @brief getTestsNotFinished If method succeeds, appends all tests which were loaded,
     * but not finished or executed e.g. because of SW/HW crash.
     * @param t List of tests, which is filled with tests, that should be executed again.
     * @return If function succeeds and no error occurs, return value is true, false otherwise.
     */
    virtual bool getTestsNotFinished(std::list<Test>& t) = 0;

    /**
     * @brief setTestHasFinished Sets flag in database, that given test has already ended.
     * @param t Test which is marked as finished.
     * @return If given test does not exists, is not running, or an error occurs,
     * return value is false, true otherwise.
     */
    virtual bool setTestHasFinished(Test t) = 0;

    /**
     * @brief setTestAsLoaded Sets flag in database, that given test has already been loaded.
     * @param t Test which is marked as loaded.
     * @return If given test does not exists, is already loaded, or an error occurs,
     * return value is false, true otherwise.
     */
    virtual bool setTestAsLoaded(const Test& t) = 0;

    /**
     * @brief updateTestForRerun Updates test to can be loaded again for rerunning.
     * @param t Test to be updated.
     * @return If an error occurs false, true otherwise.
     */
    virtual bool updateTestForRerun(const Test& t) = 0;

    /**
     * @brief setTestAsLoadedForRerun Sets flag in database, that test is loaded by the program.
     * @param t Test to be marked.
     * @return If an error occurs false, true otherwise.
     */
    virtual bool setTestAsLoadedForRerun(const Test &t) = 0;

    /**
     * @brief ~ITestManager
     */
    virtual ~ITestManager() {}
};

#endif // ITESTMANAGER

