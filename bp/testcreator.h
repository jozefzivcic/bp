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
    char** args = nullptr;
    IClassToCmdParamConverter* converter = nullptr;
    int directory;
    NistTestParameter nistParam;
    Test test;
    INistTestsManager* nistManager = nullptr;
    IFileStructureHandler* fileHandler = nullptr;
public:
    TestCreator(const ConfigStorage* stor);
    ~TestCreator();
    virtual bool createTest(int dir, Test t) override;
    virtual bool createNistTest(int dir, Test t) override;
private:
    bool execNist(int dir, Test t);
    bool waitOnChild(pid_t pid);
};

#endif // TESTCREATOR_H
