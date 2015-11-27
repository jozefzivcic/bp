#ifndef MYSQLTESTMANAGER_H
#define MYSQLTESTMANAGER_H
#include "itestmanager.h"
#include <vector>

class MySqlTestManager : public ITestManager
{
public:
    MySqlTestManager();
    virtual std::vector<Test> getAllTestsReadyForRunning() const override;
};

#endif // MYSQLTESTMANAGER_H
