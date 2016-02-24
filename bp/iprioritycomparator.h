#ifndef IPRIORITYCOMPARATOR
#define IPRIORITYCOMPARATOR
#include "test.h"

/**
 * @brief The IPriorityComparator class is used to compare two tests.
 */
class IPriorityComparator {
public:
    /**
     * @brief betterThan Compares two tests according their time of add.
     * @param t1 First test to be compared.
     * @param t2 Second test to be compared.
     * @return True if time of add of first test is less than time of add of second test.
     */
    virtual bool betterThan(const Test& t1, const Test& t2) = 0;

    /**
     * @brief ~IPriorityComparator Virtual destructor.
     */
    virtual ~IPriorityComparator() {}
};

#endif // IPRIORITYCOMPARATOR

