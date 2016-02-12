#ifndef MAINCLASS_H
#define MAINCLASS_H
#include "configparser.h"
#include "iprioritycomparator.h"
#include "ischeduler.h"
#include "configstorage.h"

class MainClass
{
private:
    ConfigParser* parser;
    IPriorityComparator* pri;
    IScheduler* scheduler;
    ConfigStorage* storage;
public:
    MainClass();
    ~MainClass();
    void run();
};

#endif // MAINCLASS_H
