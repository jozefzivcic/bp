#ifndef IRESULTSMANAGER
#define IRESULTSMANAGER
#include <iostream>
#include <test.h>

/**
 * @brief The IResultsManager class is used to store paths to directories, where results from tests
 * are saved.
 */
class IResultsManager {
public:

    /**
     * @brief storePathForTest Stores results path for test t.
     * @param t Test which path is stored.
     * @param path Path to directory, where results from test t are stored.
     * @return If an error occurs, false, true otherwise.
     */
    virtual bool storePathForTest(Test t, std::string path) = 0;

    /**
     * @brief ~IResultsManager Virtual destructor.
     */
    virtual ~IResultsManager() {}
};

#endif // IRESULTSMANAGER

