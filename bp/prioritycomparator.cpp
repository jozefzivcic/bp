#include "prioritycomparator.h"

bool PriorityComparator::betterThan(const Test &t1, const Test &t2)
{
    return t1.getTimeOfAdd() < t2.getTimeOfAdd();
}
