#ifndef INISTTESTSMANAGER
#define INISTTESTSMANAGER
#include "nisttestparameter.h"

/**
 * @brief The INistTestsManager class is used to work with database table nist_tests.
 */
class INistTestsManager {
public:

    /**
     * @brief getParameterById Searches for NistTestParameter with id as parameter and if no
     * error occurs fills param with values from database. If an error occurs, then param
     * is not changed.
     * @param id Id of NistTestParameter which is searched for.
     * @param param NistTestParameter which is filled with values from database.
     * @return If an error occurs, then false, true otherwise.
     */
    virtual bool getParameterById(long id, NistTestParameter& param) = 0;

    /**
     * @brief ~INistTestsManager Virtual destructor.
     */
    virtual ~INistTestsManager() {}
};

#endif // INISTTESTSMANAGER

