#ifndef QUEUECOMPARATOR_H
#define QUEUECOMPARATOR_H
#include "iprioritycomparator.h"

/**
 * @brief The QueueComparator class contains operator () and is used as functor in priority_queue
 * for sorting tests.
 */
class QueueComparator
{
private:

    /**
     * @brief comparator This attribute is used in this class in operator () to compare two
     * Tests.
     */
    IPriorityComparator* comparator;
public:

    /**
     * @brief QueueComparator Constructor.
     * @param comp IPriorityComparator which is used by this class.
     */
    QueueComparator(IPriorityComparator* comp);

    /**
     * @brief operator () Compares two tests according to IPriorityComparator.
     * @param t1 First test to be compared.
     * @param t2 Second test to be compared.
     * @return true, if t2 should be erased from queue earlier, false otherwise.
     */
    bool operator () (const Test& t1, const Test& t2);
};

#endif // QUEUECOMPARATOR_H
