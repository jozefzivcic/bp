#ifndef THREADHANDLER_H
#define THREADHANDLER_H
#include <vector>
#include <condition_variable>
#include "test.h"

class ThreadHandler
{
private:
    int number;
    std::vector<Test> tests;
    std::vector<std::condition_variable> vars;
    bool endThreads;
public:
    ThreadHandler();
};

#endif // THREADHANDLER_H
