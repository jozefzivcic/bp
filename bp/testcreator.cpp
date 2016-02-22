#include "testcreator.h"
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include "classtocmdparamconverter.h"
#include "mysqlnisttestsmanager.h"
#include "linuxfilestructurehandler.h"

using namespace std;

TestCreator::TestCreator(const ConfigStorage* stor) : storage(stor)
{
    converter = new ClassToCmdParamConverter(stor);
    nistManager = new MySqlNistTestsManager(stor);
    fileHandler = new LinuxFileStructureHandler(stor);
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

bool TestCreator::createTest(Test t)
{
    if (t.testTable() == storage->getNist())
        return createNistTest(t);
    return false;
}

bool TestCreator::createNistTest(Test t)
{
    NistTestParameter nistParam;
    if (!nistManager->getParameterById(t.id(), nistParam))
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
        waitOnChild(pid, t, nistParam);
        break;
    }
    return true;
}

bool TestCreator::execNist(string bin, char** argm)
{
    int ret = execv(bin.c_str(), argm);
    return ret != -1;
}

bool TestCreator::waitOnChild(pid_t pid, Test t, NistTestParameter param)
{
    pid_t returnedPid = waitpid(pid, NULL, 0);
    converter->deleteAllocatedArray(&arguments);
    if (!fileHandler->checkAndCreateUserTree(storage->getPathToUsersDirFromPool(),t.idUser()))
        return false;
    string source = fileHandler->createPathToNistResult(param.getTestNumber());
    string destination = fileHandler->createPathToStoreTest(storage->getPathToUsersDirFromPool(),
                                                            t.idUser(),t.id());
    if (!fileHandler->checkIfDirectoryExists(destination))
        if (!fileHandler->createDirectory(destination))
            return false;
    fileHandler->copyDirectoryContent(source, destination);
    return returnedPid != -1;
}
