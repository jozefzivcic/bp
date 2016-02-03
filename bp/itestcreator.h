#ifndef ITESTCREATOR
#define ITESTCREATOR
#include "test.h"

class ITestCreator {
public:
    virtual bool createTest(Test t) = 0;
    virtual bool createNistTest(Test t) = 0;
};

#endif // ITESTCREATOR

