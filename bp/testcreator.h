#ifndef TESTCREATOR_H
#define TESTCREATOR_H
#include "itestcreator.h"
#include "configstorage.h"
#include "iclasstocmdparamconverter.h"
#include "inisttestsmanager.h"
#include "ifilestructurehandler.h"

class TestCreator : public ITestCreator
{
private:
    const ConfigStorage* storage;
    char** arguments = nullptr;
    IClassToCmdParamConverter* converter = nullptr;
    INistTestsManager* nistManager = nullptr;
    IFileStructureHandler* fileHandler = nullptr;
public:
    TestCreator(const ConfigStorage* stor);
    ~TestCreator();
    virtual bool createTest(Test t) override;
    virtual bool createNistTest(Test t) override;
private:
    bool execNist(std::string bin, char **argm);
    bool waitOnChild(pid_t pid, Test t, NistTestParameter param);
};

#endif // TESTCREATOR_H
