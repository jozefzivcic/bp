#ifndef MAINCLASS_H
#define MAINCLASS_H
#include "configparser.h"
#include "iprioritycomparator.h"
#include "ischeduler.h"
#include "configstorage.h"
#include "ilogger.h"

/**
 * @brief The MainClass class is the main class of this program.
 */
class MainClass
{
private:
    int maxParallelTests;
    ConfigParser* parser = nullptr;
    IPriorityComparator* pri = nullptr;
    IScheduler* scheduler = nullptr;
    ConfigStorage* storage = nullptr;
    ILogger* logger = nullptr;
public:

    /**
     * @brief MainClass Constructor.
     */
    MainClass();

    /**
     * @brief ~MainClass Destructor.
     */
    ~MainClass();

    /**
     * @brief run This method provides main functionality of program.
     */
    void run();

    /**
     * @brief prepareEnvironment Prepares structure of files and directories, to
     * program can run properly.
     * @return If and error occurs, then false, true otherwise.
     */
    bool prepareEnvironment();
};

#endif // MAINCLASS_H
