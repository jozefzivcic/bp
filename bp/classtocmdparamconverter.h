#ifndef CLASSTOCMDPARAMCONVERTER_H
#define CLASSTOCMDPARAMCONVERTER_H
#include "iclasstocmdparamconverter.h"
#include "nistcmdparamscreator.h"
#include "ifilemanager.h"
#include "mysqlfilemanager.h"
#include "configstorage.h"
#include "inisttestsmanager.h"
#include "mysqlnisttestsmanager.h"

class ClassToCmdParamConverter :  public IClassToCmdParamConverter
{
private:
    NistCmdParamsCreator* creator = nullptr;
    IFileManager* fileManager = nullptr;
    INistTestsManager* nistManager = nullptr;
public:
    ClassToCmdParamConverter(const ConfigStorage* storage);
    ~ClassToCmdParamConverter();
    virtual bool convertNistTestToArray(char*** ptr, std::string binary, Test t) override;
    virtual bool convertNistTestToArray(char*** ptr, std::string binary, Test t, NistTestParameter param) override;
    virtual bool deleteAllocatedArray(char *** ptr) override;
};

#endif // CLASSTOCMDPARAMCONVERTER_H
