#include <iostream>
#include "ifilemanager.h"
#include "mysqlfilemanager.h"
#include "itestmanager.h"
#include "mysqltestmanager.h"
#include <list>
using namespace std;

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
    list<Test> list = testManager->getAllTestsReadyForRunning();
    for (Test t : list) {
        cout << t.id() << " " << t.idFile() << " " << t.idUser() << " " << t.timeOfAdd() << " " << t.testTable() << endl;
    }
    return 0;
}
