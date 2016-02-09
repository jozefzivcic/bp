#include "testcreator.h"
#include "constants.h"
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

bool TestCreator::createTest(Test t)
{
    if (t.testTable() == Constants::NIST)
        return createNistTest(t);
    return false;
}

bool TestCreator::createNistTest(Test t)
{
    pid_t pid = fork();
    switch(pid) {
    case 0:
        execNist(t);
        break;
    case -1:
        return false;
    default:
        waitOnChild(pid);
        break;
    }
    return true;
}

bool TestCreator::execNist(Test t)
{
    int ret = execl(Constants::PATH_TO_NIST_BINARY.c_str(), Constants::PATH_TO_NIST_BINARY.c_str(), NULL);
    return ret != -1;
}

bool TestCreator::waitOnChild(pid_t pid)
{
    pid_t returnedPid = waitpid(pid,NULL,0);
    return returnedPid != -1;
}
