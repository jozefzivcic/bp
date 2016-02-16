#include "classtocmdparamconverter.h"

using namespace std;

ClassToCmdParamConverter::ClassToCmdParamConverter(const ConfigStorage *storage)
{
    creator = new NistCmdParamsCreator();
    fileManager = new MySqlFileManager(storage);
    nistManager = new MySqlNistTestsManager(storage);
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
    NistTestParameter param;
    if (!nistManager->getParameterById(t.id(),param))
        return false;
    return convertNistTestToArray(ptr, binary, t, param);
}

bool ClassToCmdParamConverter::convertNistTestToArray(char ***ptr, string binary, Test t, NistTestParameter param)
{
    creator->resetParams();
    creator->setBinary(binary);
    File f;
    if (!fileManager->getFileById(t.idFile(), &f))
        return false;
    creator->setFile(f.fileSystemPath());
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
