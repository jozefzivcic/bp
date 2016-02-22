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
    scheduler = new Scheduler(pri, storage, maxParallelTests);
    if (!scheduler->addTestsAfterCrash())
        throw runtime_error("addTestsAfterCrash");
    scheduler->run();
}

bool MainClass::prepareEnvironment()
{
    IFileStructureHandler* handler = new LinuxFileStructureHandler(storage);
    if (!handler->controlPoolStructure(storage->getPathToTestsPool(), maxParallelTests)) {
        if (!handler->checkIfDirectoryExists(storage->getPathToTestsPool()))
            if (!handler->createDirectory(storage->getPathToTestsPool())) {
                delete handler;
                return false;
            }
        if (!handler->createCopiesOfDirectory(storage->getPathToNist(), storage->getPathToTestsPool(),
                                              maxParallelTests)) {
            delete handler;
            return false;
        }
    }
    if (!handler->checkIfDirectoryExists(storage->getPathToUsersDir()))
        if (!handler->createDirectory(storage->getPathToUsersDir())) {
            delete handler;
            return false;
        }
    delete handler;
    return true;
}
