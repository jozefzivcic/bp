#include <iostream>
#include <signal.h>
#include "mainclass.h"
#include <mutex>
#include "ilogger.h"
#include "logger.h"

using namespace std;

volatile bool endProgram = false;

void interruptHandler(int sig)
{
    (void)sig;
    endProgram = true;
}

void watchDBHandler(int sig) {
    (void)sig;
}

int main(void) {
    signal(SIGINT, interruptHandler);
    signal(SIGUSR1, watchDBHandler);
    ILogger* logger = new Logger();
    try {
        MainClass mainClass;
        if (!mainClass.prepareEnvironment())
            throw runtime_error("prepareEnvironment");
        mainClass.run();
        delete logger;
    }catch(exception& ex) {
        logger->logError(ex.what());
        delete logger;
    }
    return 0;
}
