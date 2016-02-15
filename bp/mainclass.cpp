#include "mainclass.h"
#include "prioritycomparator.h"
#include "scheduler.h"
#include "ifilestructurehandler.h"
#include "linuxfilestructurehandler.h"

using namespace std;

MainClass::MainClass()
{
    maxParallelTests = thread::hardware_concurrency() + 2;
    if (maxParallelTests == 0)
        throw runtime_error("hardware_concurrency: number of processors = 0");
    parser = new ConfigParser();
    if (!parser->parseFile("./config"))
        throw runtime_error("Config file not located or has a wrong structure");
    storage = new ConfigStorage(parser);
    pri = new PriorityComparator();
    scheduler = new Scheduler(pri, storage, maxParallelTests);
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

bool MainClass::prepareEnvironment()
{
    IFileStructureHandler* handler = new LinuxFileStructureHandler();
    if (!handler->controlFileStructure("../test_pool/", maxParallelTests))
        return handler->createCopiesOfDirectory("../tests/", "../tests_pool", maxParallelTests);
    return true;
}