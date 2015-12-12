#ifndef QUEUECOMPARATOR_H
#define QUEUECOMPARATOR_H
#include "iprioritycomparator.h"

class QueueComparator
{
private:
    IPriorityComparator* comparator;
public:
    QueueComparator(IPriorityComparator* comp);
    bool operator () (const Test& t1, const Test& t2);
};

#endif // QUEUECOMPARATOR_H
