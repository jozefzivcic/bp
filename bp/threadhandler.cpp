#include "threadhandler.h"

ThreadHandler::ThreadHandler(int n) : number(n), endThreads(false)
{
    tests.reserve(n);
    //vars.reserve(n);
}

bool ThreadHandler::setTestAndStartThread(int index, Test t)
{
    if (index >= number)
        return false;
    tests[index] = t;
    return true;
}

