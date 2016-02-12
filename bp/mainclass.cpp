#include "mainclass.h"
#include "prioritycomparator.h"
#include "scheduler.h"

using namespace std;

MainClass::MainClass()
{
    parser = new ConfigParser();
    if (!parser->parseFile("./config"))
        throw runtime_error("Config file not located or has a wrong structure");
    storage = new ConfigStorage(parser);
    pri = new PriorityComparator();
    scheduler = new Scheduler(pri,storage);
}

MainClass::~MainClass()
{
    if (scheduler != nullptr)
        delete scheduler;
    if (pri != nullptr)
        delete pri;
    if (parser != nullptr)
        delete parser;
    if (storage != nullptr)
        delete storage;
}

void MainClass::run()
{
    scheduler->run();
}

