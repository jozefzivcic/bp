#include "classtocmdparamconverter.h"

using namespace std;
ClassToCmdParamConverter::ClassToCmdParamConverter(const ConfigStorage *storage)
{
    creator = new NistCmdParamsCreator();
    fileManager = new MySqlFileManager(storage);
}

ClassToCmdParamConverter::~ClassToCmdParamConverter()
{
    if (creator != nullptr)
        delete creator;
    if (fileManager != nullptr)
        delete fileManager;
}

string ClassToCmdParamConverter::convertNistTestToCmd(Test t, NistTestParameter param)
{
    creator->resetParams();
    File f;
    fileManager->getFileById(t.idFile(), &f);
    creator->setFile(f.fileSystemPath());
    creator->setLength(param.getLength());
    if (param.getContainsStreams())
        creator->setStreams(param.getStreams());
    creator->setTest(param.getTestNumber());
    if (param.getContainsSpecialParameter())
        creator->setSpecialParameter(param.getSpecialParameter());
    return creator->getCmdParams();
}
