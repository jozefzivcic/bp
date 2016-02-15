#ifndef TESTCREATOR_H
#define TESTCREATOR_H
#include "itestcreator.h"
#include "configstorage.h"
#include "iclasstocmdparamconverter.h"

class TestCreator : public ITestCreator
{
private:
    const ConfigStorage* storage;
    char** args = nullptr;
    IClassToCmdParamConverter* converter = nullptr;
public:
    TestCreator(const ConfigStorage* stor);
    ~TestCreator();
    virtual bool createTest(std::string bin, Test t) override;
    virtual bool createNistTest(std::string bin, Test t) override;
private:
    bool execNist(std::string bin, Test t);
    bool waitOnChild(pid_t pid);
};

#endif // TESTCREATOR_H
