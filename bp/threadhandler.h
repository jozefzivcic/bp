#ifndef THREADHANDLER_H
#define THREADHANDLER_H
#include <vector>
#include <thread>
#include <condition_variable>
#include "test.h"

class ThreadHandler
{
private:
    int maxNumberOfTests;
    Test* tests = nullptr;
    bool* isThreadReady = nullptr;
    bool endThreads;
public:
    ThreadHandler(int n);
    ~ThreadHandler();
    bool setTestAtPosition(int position, Test t);
    bool getTestAtPosition(int position, Test &t);
    bool setThreadAtPositionIsReady(int position);
    bool setThreadAtPositionIsBusy(int position);
    int getIndexOfFreeThread();
    bool shouldThreadStopped();
    void stopAllThreads();

};

#endif // THREADHANDLER_H
