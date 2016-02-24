#ifndef ITESTCREATOR
#define ITESTCREATOR
#include "test.h"

/**
 * @brief The ITestCreator class creates tests and waits until tests finish. Only one test
 * can run under this class at the same time.
 */
class ITestCreator {
public:

    /**
     * @brief createTest Creates test as a new process. Select what type of process will be
     * created according to test table - test attribute.
     * @param bin Path to executable file.
     * @param t Test, which holds all data needed for test creation.
     * @return If an error occurs false, true otherwise.
     */
    virtual bool createTest(Test t) = 0;

    /**
     * @brief createNistTest Creates a NIST test.
     * @param bin Path to executable file.
     * @param t Data for test.
     * @return If an error occurs false, true otherwise.
     */
    virtual bool createNistTest(Test t) = 0;

    /**
     * @brief ~ITestCreator Virtual destructor.
     */
    virtual ~ITestCreator() {}
};

#endif // ITESTCREATOR

