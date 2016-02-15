#ifndef INISTTESTSMANAGER
#define INISTTESTSMANAGER
#include "nisttestparameter.h"

class INistTestsManager {
public:
    virtual bool getParameterById(long id, NistTestParameter& param) = 0;
    virtual ~INistTestsManager() {}
};

#endif // INISTTESTSMANAGER

