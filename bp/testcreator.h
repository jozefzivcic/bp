#ifndef TESTCREATOR_H
#define TESTCREATOR_H
#include "itestcreator.h"

class TestCreator : public ITestCreator
{
public:
    TestCreator();
    virtual bool createTest(Test t) override;
    virtual bool createNistTest(Test t) override;
};

#endif // TESTCREATOR_H
