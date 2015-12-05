#include <iostream>
#include "ifilemanager.h"
#include "mysqlfilemanager.h"
#include "itestmanager.h"
#include "mysqltestmanager.h"
#include <list>
#include "icurrentlyrunningmanager.h"
#include "mysqlcurrentlyrunningmanager.h"

using namespace std;

void printTests(list<Test> l) {
    for (Test t : l) {
        cout << t.id() << " " << t.idFile() << " " << t.idUser() << " " << t.timeOfAdd() << " " << t.testTable() << endl;
    }
}

int main(void) {
    IFileManager* fileManager = new MySqlFileManager();
    File f;
    bool res = fileManager->getFileById(2,&f);
    if (res)
        cout << f.id() << " " << f.userId() << " " << f.hash() << " " << f.name() << " " << f.fileSystemPath() << endl;
    else
        cout << "Error" << endl;
    delete fileManager;
    ITestManager* testManager = new MySqlTestManager();
    list<Test> l = testManager->getAllTestsReadyForRunning();
    printTests(l);
    ICurrentlyRunningManager* crManager = new MySqlCurrentlyRunningManager();
    crManager->insertTest(l.front());
    testManager->setTestHasStarted(l.front());
    printTests(testManager->getAllTestsReadyForRunning());
    getchar();
    crManager->removeTest(l.front());
    delete testManager;
    delete crManager;
    return 0;
}
