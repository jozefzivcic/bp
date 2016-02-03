#include "threadhandler.h"

using namespace std;

ThreadHandler::ThreadHandler(int n) : number(n), endThreads(false)
{
    tests = new Test[n];
    mutexes = new mutex[n];
    vars = new condition_variable[n];
    isThreadReady = new bool[n];
    endThreads = false;
}

ThreadHandler::~ThreadHandler()
{
    delete[] tests;
    delete[] mutexes;
    delete[] vars;
    delete[] isThreadReady;
}

bool ThreadHandler::setTestAtPosition(int position, Test t)
{
    if (position >= number)
        return false;
    tests[position] = t;
    return true;
}

bool ThreadHandler::getMutexAtPosition(int position, mutex &m)
{

}

bool ThreadHandler::getConditionVariableAtPosition(int position, condition_variable &var)
{

}

bool ThreadHandler::setThreadAtPositionIsReady(int position)
{

}

bool ThreadHandler::setThreadAtPositionIsBusy(int position)
{

}

int ThreadHandler::findFreeThread()
{

}

void ThreadHandler::stopAllThreads()
{

}



