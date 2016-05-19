#ifndef IPRIORITYCOMPARATOR
#define IPRIORITYCOMPARATOR
#include "test.h"

/**
 * @brief The IPriorityComparator class is used to compare two tests.
 */
class IPriorityComparator {
public:
    /**
     * @brief betterThan Compares two tests which has better priority.
     * @param t1 First test to be compared.
     * @param t2 Second test to be compared.
     * @return True first test has better priority than second test.
     */
    virtual bool betterThan(const Test& t1, const Test& t2) = 0;

    /**
     * @brief ~IPriorityComparator Virtual destructor.
     */
    virtual ~IPriorityComparator() {}
};

#endif // IPRIORITYCOMPARATOR

