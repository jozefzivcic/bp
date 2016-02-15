#include "testcreator.h"
#include "constants.h"
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

TestCreator::TestCreator(const ConfigStorage* stor) : storage(stor) {}

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
    int ret = execl(storage->getPathToNist().c_str(), storage->getPathToNist().c_str(), NULL);
    return ret != -1;
}

bool TestCreator::waitOnChild(pid_t pid)
{
    pid_t returnedPid = waitpid(pid,NULL,0);
    return returnedPid != -1;
}
