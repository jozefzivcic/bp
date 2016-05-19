#ifndef NISTCMDPARAMSCREATOR_H
#define NISTCMDPARAMSCREATOR_H
#include "ilogger.h"
#include <iostream>
#include <list>

/**
 * @brief The NistCmdParamsCreator class creates parameters for NIST tests.
 */
class NistCmdParamsCreator
{
private:

    /**
     * @brief params Contains cmd line parameters.
     */
    std::list<std::string> params;

    /**
     * @brief testNumber Contains for which test are created parameters.
     */
    int testNumber;

    /**
     * @brief logger Logging class.
     */
    ILogger* logger;
public:

    /**
     * @brief NistCmdParamsCreator Constructor, creates parameters with only flag: -fast.
     */
    NistCmdParamsCreator();

    /**
     * @brief ~NistCmdParamsCreator Destructor.
     */
    ~NistCmdParamsCreator();

    /**
     * @brief getCmdParams Getter.
     * @return String with setted options.
     */
    std::string getCmdParams() const;

    /**
     * @brief resetParams Deletes all setted options except -fast.
     */
    void resetParams();

    /**
     * @brief setBinary Sets binary to be executed as 0th argument.
     * @param bin Filesystem path to binary.
     */
    void setBinary(std::string bin);

    /**
     * @brief setLength Adds -length option.
     * @param length Parameter of switch -length.
     */
    void setLength(long length);

    /**
     * @brief setFile Adds -file option.
     * @param file Parameter of switch -file.
     */
    void setFile(std::string file);

    /**
     * @brief setStreams Adds -streams option.
     * @param streams Parameter of switch -streams.
     */
    void setStreams(long streams);

    /**
     * @brief setTest Adds -tests option.
     * @param test Number of test.
     * @return true if param test is in range from 1 to 15, false otherwise.
     */
    bool setTest(int test);

    /**
     * @brief setSpecialParameter Adds option -blockfreqpar or -nonoverpar or -overpar or
     * -approxpar or -serialpar or -linearpar. This method must be called after setTest.
     * @param param Parameter to option -blockfreqpar ...
     * @return true if method was called after setTest, false otherwise.
     */
    bool setSpecialParameter(long param);

    /**
     * @brief fillArrayOfArguments Allocates memory to pointer ptr and then fills array with
     * parameters set with methods above.
     * @param ptr Pointer to array, that will hold parameters.
     * @return if given pointer is nullptr then false, true otherwise.
     */
    bool fillArrayOfArguments(char*** ptr);

    /**
     * @brief deleteArrayOfArguments Frees allocated space on pointer ptr.
     * @param ptr Pointer to array to be freed.
     * @return if given pointer is nullptr then false, true otherwise.
     */
    bool deleteArrayOfArguments(char*** ptr);
private:

    /**
     * @brief convertLongToString Converts long to string.
     * @param n Long number to be converted.
     * @return String representation of long parameter.
     */
    std::string convertLongToString(long n);
};

#endif // NISTCMDPARAMSCREATOR_H
