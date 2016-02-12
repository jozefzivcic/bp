#ifndef TESTCREATOR_H
#define TESTCREATOR_H
#include "itestcreator.h"
#include "configstorage.h"

class TestCreator : public ITestCreator
{
private:
    const ConfigStorage* storage;
public:
    TestCreator(const ConfigStorage* stor);
    virtual bool createTest(Test t) override;
    virtual bool createNistTest(Test t) override;
private:
    bool execNist(Test t);
    bool waitOnChild(pid_t pid);
};

#endif // TESTCREATOR_H
