#ifndef THREADHANDLER_H
#define THREADHANDLER_H
#include <vector>
#include <thread>
#include <condition_variable>
#include "test.h"

/**
 * @brief The ThreadHandler class is used to manipulate with parameters for threads.
 */
class ThreadHandler
{
private:
    int maxNumberOfTests;
    Test* tests = nullptr;
    bool* isThreadReady = nullptr;
    bool endThreads;
public:
    /**
     * @brief ThreadHandler Constructor.
     * @param n Maximum number of tests that can run in parallel.
     */
    ThreadHandler(int n);
    ~ThreadHandler();

    /**
     * @brief setTestAtPosition Sets test at position to t.
     * @param position Position at which test is set.
     * @param t Test that is set at position position.
     * @return If position is greater or equal to maxNumberOfTests then false, true otherwise.
     */
    bool setTestAtPosition(int position, Test t);

    /**
     * @brief getTestAtPosition Gets test at position position. If position is not valid,
     * Test t remains untouched.
     * @param position Position from which test is returned.
     * @param t Variable that will be filled according to Test at position position.
     * @return If position is greater or equal to maxNumberOfTests then false, true otherwise.
     */
    bool getTestAtPosition(int position, Test &t);

    /**
     * @brief setThreadAtPositionIsReady Sets that thread at position is ready to execute test.
     * @param position Position of thread.
     * @return If position is greater or equal to maxNumberOfTests then false, true otherwise.
     */
    bool setThreadAtPositionIsReady(int position);

    /**
     * @brief setThreadAtPositionIsBusy Sets that thread at position is busy and cannot execute
     * test.
     * @param position Position of thread.
     * @return If position is greater or equal to maxNumberOfTests then false, true otherwise.
     */
    bool setThreadAtPositionIsBusy(int position);

    /**
     * @brief getIndexOfFreeThread Finds first free thread that can execute test.
     * @return Position of thread that is ready or -1 of all threads are busy.
     */
    int getIndexOfFreeThread();

    /**
     * @brief shouldThreadStop Getter that returns if all thread should stop.
     * @return True if all threads should stop, false otherwise.
     */
    bool shouldThreadStop();

    /**
     * @brief stopAllThreads Sets attribute that in next call of shouldThreadStopped() it
     * returns true.
     */
    void stopAllThreads();

};

#endif // THREADHANDLER_H
