#ifndef TESTCREATOR_H
#define TESTCREATOR_H
#include "itestcreator.h"
#include "configstorage.h"
#include "iclasstocmdparamconverter.h"
#include "inisttestsmanager.h"
#include "ifilestructurehandler.h"
#include "iresultsmanager.h"
#include "mysqldbpool.h"
#include "ilogger.h"
#include "itestmanager.h"

/**
 * @brief The TestCreator class implements interface ITestCreator. For methods comments see the
 * interface.
 */
class TestCreator : public ITestCreator
{
private:
    const ConfigStorage* storage;

    /**
     * @brief arguments Array of arguments, which are used in execv.
     */
    char** arguments = nullptr;
    IClassToCmdParamConverter* converter = nullptr;
    INistTestsManager* nistManager = nullptr;
    IFileStructureHandler* fileHandler = nullptr;
    IResultsManager* resManager = nullptr;
    MySqlDBPool* dbPool = nullptr;
    ILogger* logger = nullptr;
    ITestManager* testManager = nullptr;
public:
    TestCreator(const ConfigStorage* stor, MySqlDBPool* pool);
    ~TestCreator();
    virtual bool createTest(Test t) override;
    virtual bool createNistTest(Test t) override;
private:

    /**
     * @brief execNist Calls execv function on binary bin with parameters argm.
     * @param bin File which is executed.
     * @param argm Command line arguments.
     * @return If execv fails then false, nothing otherwise.
     */
    bool execNist(std::string bin, char **argm);

    /**
     * @brief waitOnNistChild Waits on child process, that represents NIST test.
     * @param pid pid_t of process for which is waited.
     * @param t Test which is associated with process with pid.
     * @param param NistTestParameter which is associated with test t.
     * @return If an error occurs false, true otherwise.
     */
    bool waitOnNistChild(pid_t pid, Test t, NistTestParameter param);

    /**
     * @brief extractFromStatus Extracts info from status and fills other variables.
     * @param status Status from waitpid.
     * @param ret Variable which is filled with return value of process.
     * @param signaled If child process was ended using signal.
     */
    void extractFromStatus(const int& status, int& ret, int& signaled);

    /**
     * @brief addSecondsToTime Adds seconds to given time.
     * @param time Base time.
     * @param seconds Seconds to be added.
     * @return New time.
     */
    time_t addSecondsToTime(time_t time, unsigned int seconds);
};

#endif // TESTCREATOR_H
