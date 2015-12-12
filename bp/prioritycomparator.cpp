#include "prioritycomparator.h"

bool PriorityComparator::betterThan(const Test &t1, const Test &t2)
{
    return t1.timeOfAdd() < t2.timeOfAdd();
}
