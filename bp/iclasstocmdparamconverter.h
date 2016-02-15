#ifndef ICLASSTOCMDPARAMCONVERTER
#define ICLASSTOCMDPARAMCONVERTER
#include "nisttestparameter.h"
#include "test.h"
#include <iostream>

class IClassToCmdParamConverter {
public:
    virtual bool convertNistTestToArray(char*** ptr, std::string binary, Test t) = 0;
    virtual bool deleteAllocatedArray(char*** ptr) = 0;
    virtual ~IClassToCmdParamConverter() {}
};

#endif // ICLASSTOCMDPARAMCONVERTER

