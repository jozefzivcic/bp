#include <iostream>
#include <signal.h>
#include "mainclass.h"

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
    try {
        MainClass mainClass;
        if (!mainClass.prepareEnvironment())
            throw runtime_error("prepareEnvironment");
        mainClass.run();
    }catch(exception ex) {
        cout << "Unexpected program end" << endl;
        cout << ex.what() << endl;
    }
    return 0;
}
