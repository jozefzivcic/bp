#ifndef ICLASSTOCMDPARAMCONVERTER
#define ICLASSTOCMDPARAMCONVERTER
#include "nisttestparameter.h"
#include "test.h"
#include <iostream>

class IClassToCmdParamConverter {
public:
    virtual std::string convertNistTestToCmd(Test t, NistTestParameter param) = 0;
};

#endif // ICLASSTOCMDPARAMCONVERTER

