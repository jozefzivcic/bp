#include "testcreator.h"
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include "classtocmdparamconverter.h"

TestCreator::TestCreator(const ConfigStorage* stor) : storage(stor)
{
    converter = new ClassToCmdParamConverter(stor);
}

TestCreator::~TestCreator()
{
    if (converter != nullptr)
        delete converter;
}

bool TestCreator::createTest(std::string bin, Test t)
{
    if (t.testTable() == storage->getNist())
        return createNistTest(bin, t);
    return false;
}

bool TestCreator::createNistTest(std::string bin, Test t)
{
    pid_t pid = fork();
    switch(pid) {
    case 0:
        execNist(bin, t);
        break;
    case -1:
        return false;
    default:
        waitOnChild(pid);
        break;
    }
    return true;
}

bool TestCreator::execNist(std::string bin, Test t)
{
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
