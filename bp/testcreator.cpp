#include "testcreator.h"
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sched.h>
#include "classtocmdparamconverter.h"
#include "mysqlnisttestsmanager.h"
#include "linuxfilestructurehandler.h"

using namespace std;

TestCreator::TestCreator(const ConfigStorage* stor) : storage(stor), directory(0)
{
    converter = new ClassToCmdParamConverter(stor);
    nistManager = new MySqlNistTestsManager(stor);
    fileHandler = new LinuxFileStructureHandler();
}

TestCreator::~TestCreator()
{
    if (converter != nullptr)
        delete converter;
    if (nistManager != nullptr)
        delete nistManager;
    if (fileHandler != nullptr)
        delete fileHandler;
}

bool TestCreator::createTest(int dir, Test t)
{
    if (t.testTable() == storage->getNist())
        return createNistTest(dir, t);
    return false;
}

bool TestCreator::createNistTest(int dir, Test t)
{
    //pid_t pid = fork();
    execNist(dir, t);
//    switch(pid) {
//    case 0:
//        execNist(dir, t);
//        break;
//    case -1:
//        return false;
//    default:
//        waitOnChild(pid);
//        break;
//    }
    return true;
}

bool TestCreator::execNist(int dir, Test t)
{
    directory = dir;
    test = t;
    if (!nistManager->getParameterById(t.id(), nistParam))
        return false;
    list<string> l;
    l.push_back(storage->getPathToTestsPool());
    l.push_back(to_string(dir));
    l.push_back("assess");
    string bin = fileHandler->createFSPath(false, l);
    unshare(CLONE_FS);
    chdir(bin.c_str());
    bin = "./assess";
    if (!converter->convertNistTestToArray(&arguments, bin, t, nistParam))
        return false;
    int ret = execv(bin.c_str(), arguments);
    return ret != -1;
}

bool TestCreator::waitOnChild(pid_t pid)
{
    pid_t returnedPid = waitpid(pid, NULL, 0);
    converter->deleteAllocatedArray(&arguments);
    string source = fileHandler->createPathToNistResult(storage->getPathToTestsPool(),
                                                        directory, nistParam.getTestNumber());
    string destination = fileHandler->createPathToStoreTest(storage->getPathToUsersDir(),
                                                            test.idUser(),test.id());
    fileHandler->copyDirectory(source, destination);
    return returnedPid != -1;
}
