#include "testcreator.h"
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include "classtocmdparamconverter.h"

using namespace std;

TestCreator::TestCreator(const ConfigStorage* stor) : storage(stor), directory(0)
{
    converter = new ClassToCmdParamConverter(stor);
}

TestCreator::~TestCreator()
{
    if (converter != nullptr)
        delete converter;
}

bool TestCreator::createTest(int dir, Test t)
{
    if (t.testTable() == storage->getNist())
        return createNistTest(dir, t);
    return false;
}

bool TestCreator::createNistTest(int dir, Test t)
{
    pid_t pid = fork();
    switch(pid) {
    case 0:
        execNist(dir, t);
        break;
    case -1:
        return false;
    default:
        waitOnChild(pid);
        break;
    }
    return true;
}

bool TestCreator::execNist(int dir, Test t)
{
    directory = dir;
    string bin = storage->getPathToTestsPool();
    if (bin[bin.length() - 1] != '/')
        bin += "/";
    bin += to_string(dir);
    bin += "/assess";
    if (!converter->convertNistTestToArray(&args, bin, t))
        return false;
    int ret = execv(bin.c_str(), args);
    return ret != -1;
}

bool TestCreator::waitOnChild(pid_t pid)
{
    pid_t returnedPid = waitpid(pid,NULL,0);
    converter->deleteAllocatedArray(&args);
    return returnedPid != -1;
}
