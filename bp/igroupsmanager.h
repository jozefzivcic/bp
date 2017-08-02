#ifndef IGROUPSMANAGER_H
#define IGROUPSMANAGER_H
#include "test.h"

/**
 * @brief The IGroupManager class is interface which is used to work with table groups
 * in database.
 */
class IGroupsManager {
public:

    /**
     * @brief increaseFinishedTests Increments column finished_tests by one in row associated to
     * group of test t. This method should be called only after test finishes normally.
     * @param t Test for which group finished_tests should be incremented.
     * @return If an error occurs false, true otherwise.
     */
    virtual bool increaseFinishedTests(Test t) = 0;

    /**
     * @brief ~IGroupsManager Virtual destructor.
     */
    virtual ~IGroupsManager() {}
};

#endif // IGROUPSMANAGER_H
