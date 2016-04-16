#include "testcreator.h"
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include "classtocmdparamconverter.h"
#include "mysqlnisttestsmanager.h"
#include "linuxfilestructurehandler.h"
#include "mysqlresultsmanager.h"
#include "logger.h"
#include "mysqltestmanager.h"
#include <string>

using namespace std;

TestCreator::TestCreator(const ConfigStorage* stor, MySqlDBPool* pool) : storage(stor)
{
    dbPool = pool;
    converter = new ClassToCmdParamConverter(stor, dbPool);
    nistManager = new MySqlNistTestsManager(dbPool);
    fileHandler = new LinuxFileStructureHandler(stor);
    resManager = new MySqlResultsManager(dbPool);
    testManager = new MySqlTestManager(dbPool);
    logger = new Logger();
}

TestCreator::~TestCreator()
{
    if (converter != nullptr)
        delete converter;
    if (nistManager != nullptr)
        delete nistManager;
    if (fileHandler != nullptr)
        delete fileHandler;
    if (resManager != nullptr)
        delete resManager;
    if (logger != nullptr)
        delete logger;
    if (testManager != nullptr)
        delete testManager;
}

bool TestCreator::createTest(Test t)
{
    if (t.getTestTable() == storage->getNist())
        return createNistTest(t);
    return false;
}

bool TestCreator::createNistTest(Test t)
{
    NistTestParameter nistParam;
    if (!nistManager->getParameterById(t.getId(), nistParam))
        return false;

    string bin = "./assess";
    if (!converter->convertNistTestToArray(&arguments, bin, t, nistParam))
        return false;
    pid_t pid = fork();

    switch(pid) {
    case 0:
        execNist(bin, arguments);
        break;
    case -1:
        return false;
    default:
        waitOnNistChild(pid, t, nistParam);
        break;
    }
    return true;
}

bool TestCreator::execNist(string bin, char** argm)
{
    int ret = execv(bin.c_str(), argm);
    return ret != -1;
}

bool TestCreator::waitOnNistChild(pid_t pid, Test t, NistTestParameter param)
{
    int status = 0;
    waitpid(pid, &status, 0);
    int returnValue, signaled;
    extractFromStatus(status, returnValue, signaled);
    converter->deleteAllocatedArray(&arguments);
    t.increaseRuns();
    t.setReturnValue(returnValue);
    if ((returnValue != 1 || signaled != 0) && t.getNumOfRuns() < storage->getRerunTimes()) {
        t.setTimeOfRerun(addSecondsToTime(time(0), storage->getRerunAfter()));
        testManager->updateTestForRerun(t);
        return true;
    }
    if (!fileHandler->checkAndCreateUserTree(storage->getPathToUsersDirFromPool(),t.getUserId()))
        return false;
    string source = fileHandler->createPathToNistResult(param.getTestNumber());
    string destination = fileHandler->createPathToStoreTest(storage->getPathToUsersDirFromPool(),
                                                            t.getUserId(),t.getId());
    if (!fileHandler->checkIfDirectoryExists(destination))
        if (!fileHandler->createDirectory(destination))
            return false;
    fileHandler->copyDirectory(source, destination, false);
    string absPath = fileHandler->getAbsolutePath(destination);
    resManager->storePathForTest(t, absPath);
    testManager->setTestHasFinished(t);
    return true;
}

void TestCreator::extractFromStatus(const int &status, int &ret, int &signaled)
{
    ret = WEXITSTATUS(status);
    signaled = WIFSIGNALED(status);
}

time_t TestCreator::addSecondsToTime(time_t time, unsigned int seconds)
{
    return time + seconds;
}
