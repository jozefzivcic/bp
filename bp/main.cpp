#include <iostream>
#include "ifilemanager.h"
#include "mysqlfilemanager.h"
#include "itestmanager.h"
#include "mysqltestmanager.h"
#include <list>
#include "icurrentlyrunningmanager.h"
#include "mysqlcurrentlyrunningmanager.h"
#include <thread>
#include "queuecomparator.h"
#include "prioritycomparator.h"
#include <queue>
#include <vector>
#include "scheduler.h"
using namespace std;

void printTests(list<Test> l) {
    for (Test t : l) {
        cout << t.id() << " " << t.idFile() << " " << t.idUser() << " " << t.timeOfAdd() << " " << t.testTable() << endl;
    }
}

void printFile(File f) {
    cout << f.id() << " " << f.userId() << " " << f.hash() << " " << f.name() << " " << f.fileSystemPath() << endl;
}

int main(void) {
    /*
    IFileManager* fileManager = new MySqlFileManager();
    File f;
    bool res = fileManager->getFileById(2,&f);
    if (res)
        printFile(f);
    else
        cout << "Error" << endl;
    delete fileManager;
    ITestManager* testManager = new MySqlTestManager();
    list<Test> l;
    if (testManager->getAllTestsReadyForRunning(l))
        printTests(l);
    else
        cout << "ERROR: getAllTestsReadyForRunning()" << endl;
    ICurrentlyRunningManager* crManager = new MySqlCurrentlyRunningManager();
    crManager->insertTest(l.front());
    l.front().setId(45);
    if (!testManager->setTestHasStarted(l.front()))
        cout << "Error setTestHasStarted" << endl;
    list<Test> testsAfterSomeAreRunning;
    cout << "-------" << endl;
    if (testManager->getAllTestsReadyForRunning(testsAfterSomeAreRunning))
        printTests(testsAfterSomeAreRunning);
    else
        cout << "ERROR: getAllTestsReadyForRunning()" << endl;
    getchar();
    testManager->setTestHasFinished(l.front());
    crManager->removeTest(l.front());
    delete testManager;
    delete crManager;
*/
    IPriorityComparator* pri = new PriorityComparator();
    Scheduler s(pri);
    s.getTestForRunning();
    return 0;
}
