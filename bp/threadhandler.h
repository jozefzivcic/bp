#ifndef THREADHANDLER_H
#define THREADHANDLER_H
#include <vector>
#include <thread>
#include <condition_variable>
#include "test.h"

class ThreadHandler
{
private:
    int number;
    Test* tests;
    std::mutex* mutexes;
    std::condition_variable* vars;
    bool* isThreadReady;
    bool endThreads;
public:
    ThreadHandler(int n);
    ~ThreadHandler();
    bool setTestAtPosition(int position, Test t);
    bool getMutexAtPosition(int position, std::mutex& m);
    bool getConditionVariableAtPosition(int position, std::condition_variable& var);
    bool setThreadAtPositionIsReady(int position);
    bool setThreadAtPositionIsBusy(int position);
    int findFreeThread();
    void stopAllThreads();

};

#endif // THREADHANDLER_H
