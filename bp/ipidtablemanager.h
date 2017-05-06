#ifndef IPIDTABLEMANAGER
#define IPIDTABLEMANAGER
#include <sys/types.h>

/**
 * @brief The IPIDTableManager class is used to store and remove pid of some process into table called pid_table.
 */
class IPIDTableManager {
public:

    /**
     * @brief storePIDForId Stores given pid with id.
     * @param id Id of pid.
     * @param pid Process identification number to store.
     * @return If an error occurs false, true otherwise.
     */
    virtual bool storePIDForId(long id, int pid) = 0;

    /**
     * @brief removePIDForId Removes pid with id from table.
     * @param id ID of pid to be removed.
     * @return If an error occurs false, true otherwise.
     */
    virtual bool removePIDForId(long id) = 0;

    /**
     * @brief getPIDForId Fills parameter pid according to record in database with identificator id.
     * @param id Identificator for record in database.
     * @param pid This variable is filled with pid that is stored in database.
     * @return If record with identificator id exists, then this method returns true and variable pid is filled.
     * If no record for identificator id exists, this method returns false and variable pid is not changed.
     */
    virtual bool getPIDForId(long id, pid_t& pid) = 0;

    /**
     * @brief ~IPIDTableManager Virtual destructor.
     */
    virtual ~IPIDTableManager() {}
};

#endif // IPIDTABLEMANAGER

