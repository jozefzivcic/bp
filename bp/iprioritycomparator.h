#ifndef IPRIORITYCOMPARATOR
#define IPRIORITYCOMPARATOR
#include "test.h"
class IPriorityComparator {
public:
    virtual bool betterThan(const Test& t1, const Test& t2) = 0;
    virtual ~IPriorityComparator() {}
};

#endif // IPRIORITYCOMPARATOR

