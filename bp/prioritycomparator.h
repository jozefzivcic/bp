#ifndef PRIORITYCOMPARATOR_H
#define PRIORITYCOMPARATOR_H
#include "iprioritycomparator.h"

class PriorityComparator : public IPriorityComparator
{
public:
    virtual bool betterThan(const Test& t1, const Test& t2) override;
};

#endif // PRIORITYCOMPARATOR_H
