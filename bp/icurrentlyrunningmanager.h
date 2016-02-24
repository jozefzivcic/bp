#ifndef ICURRENTLYRUNNINGMANAGER
#define ICURRENTLYRUNNINGMANAGER
#include "test.h"

/**
 * @brief The ICurrentlyRunningManager class manages database table currently_running.
 */
class ICurrentlyRunningManager {
public:

    /**
     * @brief insertTest Inserts test id into table currently_running.
     * @param t Test which id will be added into the table.
     * @return true if insertion was successful, false otherwise.
     */
    virtual bool insertTest(Test t) = 0;

    /**
     * @brief removeTest Removes test id from table currently_running.
     * @param t Test which id will be deleted from table.
     * @return true if insertion was successful, false otherwise.
     */
    virtual bool removeTest(Test t) = 0;

    /**
     * @brief ~ICurrentlyRunningManager Virtual destructor.
     */
    virtual ~ICurrentlyRunningManager() {}
};

#endif // ICURRENTLYRUNNINGMANAGER

