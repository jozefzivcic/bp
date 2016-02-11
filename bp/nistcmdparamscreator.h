#ifndef NISTCMDPARAMSCREATOR_H
#define NISTCMDPARAMSCREATOR_H
#include <iostream>

class NistCmdParamsCreator
{
private:

    /**
     * @brief params Contains cmd line parameters.
     */
    std::string params;

    /**
     * @brief testNumber Contains for which test are created parameters.
     */
    int testNumber;
public:

    /**
     * @brief NistCmdParamsCreator Constructor, creates parameters with only flag: -fast.
     */
    NistCmdParamsCreator();

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
private:

    /**
     * @brief convertLongToString Converts long to string.
     * @param n Long number to be converted.
     * @return String representation of long parameter.
     */
    std::string convertLongToString(long n);
};

#endif // NISTCMDPARAMSCREATOR_H
