#include "classtocmdparamconverter.h"

using namespace std;

ClassToCmdParamConverter::ClassToCmdParamConverter(const ConfigStorage *configStorage, MySqlDBPool *pool)
{
    dbPool = pool;
    creator = new NistCmdParamsCreator();
    fileManager = new MySqlFileManager(dbPool);
    nistManager = new MySqlNistTestsManager(dbPool);
    storage = configStorage;
}

ClassToCmdParamConverter::~ClassToCmdParamConverter()
{
    if (creator != nullptr)
        delete creator;
    if (fileManager != nullptr)
        delete fileManager;
    if (nistManager != nullptr)
        delete nistManager;
}

bool ClassToCmdParamConverter::convertNistTestToArray(char ***ptr, string binary, Test t)
{
    if (t.getTestTable() != storage->getNist())
        return false;
    NistTestParameter param;
    if (!nistManager->getParameterById(t.getId(),param))
        return false;
    return convertNistTestToArray(ptr, binary, t, param);
}

bool ClassToCmdParamConverter::convertNistTestToArray(char ***ptr, string binary, Test t, NistTestParameter param)
{
    if (t.getTestTable() != storage->getNist())
        return false;
    creator->resetParams();
    creator->setBinary(binary);
    File f;
    if (!fileManager->getFileById(t.getFileId(), &f))
        return false;
    creator->setFile(f.getFileSystemPath());
    creator->setLength(param.getLength());
    if (param.getContainsStreams())
        creator->setStreams(param.getStreams());
    creator->setTest(param.getTestNumber());
    if (param.getContainsSpecialParameter())
        creator->setSpecialParameter(param.getSpecialParameter());
    return creator->fillArrayOfArguments(ptr);
}

bool ClassToCmdParamConverter::deleteAllocatedArray(char ***ptr)
{
    return creator->deleteArrayOfArguments(ptr);
}
