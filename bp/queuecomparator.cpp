#include "queuecomparator.h"

QueueComparator::QueueComparator(IPriorityComparator *comp) : comparator(comp) {}

bool QueueComparator::operator ()(const Test &t1, const Test &t2)
{
    return comparator->betterThan(t2,t1);
}

