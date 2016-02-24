#ifndef MAINCLASS_H
#define MAINCLASS_H
#include "configparser.h"
#include "iprioritycomparator.h"
#include "ischeduler.h"
#include "configstorage.h"
#include "ilogger.h"

class MainClass
{
private:
    int maxParallelTests;
    ConfigParser* parser = nullptr;
    IPriorityComparator* pri = nullptr;
    IScheduler* scheduler = nullptr;
    ConfigStorage* storage = nullptr;
    ILogger* logger = nullptr;
public:
    MainClass();
    ~MainClass();
    void run();
    bool prepareEnvironment();
};

#endif // MAINCLASS_H
