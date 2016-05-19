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
    /**
     * @brief betterThan Compares two tests according their time of add.
     * @param t1 First test to be compared.
     * @param t2 Second test to be compared.
     * @return True if time of add of first test is less than time of add of second test.
     */
    virtual bool betterThan(const Test& t1, const Test& t2) override;
};

#endif // PRIORITYCOMPARATOR_H
