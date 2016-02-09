#include <iostream>
#include <signal.h>
#include "iprioritycomparator.h"
#include "prioritycomparator.h"
#include "ischeduler.h"
#include "scheduler.h"

using namespace std;

bool endProgram = false;

void interruptHandler(int sig)
{
    (void)sig;
    endProgram = true;
    cout << "signal" << endl;
}

int main(void) {
    signal(SIGINT,interruptHandler);
    IPriorityComparator* pri = new PriorityComparator();
    IScheduler* scheduler = new Scheduler(pri);
    scheduler->run();
    delete scheduler;
    delete pri;
    return 0;
}
