#ifndef PRIORITYCOMPARATOR_H
#define PRIORITYCOMPARATOR_H
#include "iprioritycomparator.h"

/**
 * @brief The PriorityComparator class is implementation of interface IPriorityComparator. For
 * method documentation see interface.
 */
class PriorityComparator : public IPriorityComparator
{
public:
    virtual bool betterThan(const Test& t1, const Test& t2) override;
};

#endif // PRIORITYCOMPARATOR_H
