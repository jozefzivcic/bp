#include "threadhandler.h"

using namespace std;

ThreadHandler::ThreadHandler(int n) : maxNumberOfTests(n), endThreads(false)
{
    tests = new Test[n];
    isThreadReady = new bool[n];
    for (int i = 0; i < n; i++) {
        isThreadReady[i] = false;
    }
    endThreads = false;
}

ThreadHandler::~ThreadHandler()
{
    if (tests != nullptr)
        delete[] tests;
    if (isThreadReady != nullptr)
        delete[] isThreadReady;
}

bool ThreadHandler::setTestAtPosition(int position, Test t)
{
    if (position >= maxNumberOfTests)
        return false;
    tests[position] = t;
    return true;
}

bool ThreadHandler::getTestAtPosition(int position, Test& t)
{
    if (position >= maxNumberOfTests)
        return false;
    t = tests[position];
    return true;
}

bool ThreadHandler::setThreadAtPositionIsReady(int position)
{
    if (position >= maxNumberOfTests)
        return false;
    isThreadReady[position] = true;
    return true;
}

bool ThreadHandler::setThreadAtPositionIsBusy(int position)
{
    if (position >= maxNumberOfTests)
        return false;
    isThreadReady[position] = false;
    return true;
}

int ThreadHandler::getIndexOfFreeThread()
{
    int i = 0;
    while (!isThreadReady[i] && i < maxNumberOfTests)
        i++;
    if (i != maxNumberOfTests)
        return i;
    return -1;
}

bool ThreadHandler::shouldThreadStopped()
{
    return endThreads;
}

void ThreadHandler::stopAllThreads()
{
    endThreads = true;
}
