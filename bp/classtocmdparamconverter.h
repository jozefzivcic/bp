#ifndef CLASSTOCMDPARAMCONVERTER_H
#define CLASSTOCMDPARAMCONVERTER_H
#include "iclasstocmdparamconverter.h"
#include "nistcmdparamscreator.h"
#include "ifilemanager.h"
#include "mysqlfilemanager.h"
#include "configstorage.h"

class ClassToCmdParamConverter :  public IClassToCmdParamConverter
{
private:
    NistCmdParamsCreator* creator = nullptr;
    IFileManager* fileManager = nullptr;
public:
    ClassToCmdParamConverter(const ConfigStorage* storage);
    ~ClassToCmdParamConverter();
    virtual std::string convertNistTestToCmd(Test t, NistTestParameter param) override;
};

#endif // CLASSTOCMDPARAMCONVERTER_H
