#ifndef IPIDTABLEMANAGER
#define IPIDTABLEMANAGER

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
    virtual bool storePIDForId(int id, int pid) = 0;

    /**
     * @brief removePIDForId Removes pid with id from table.
     * @param id ID of pid to be removed.
     * @return If an error occurs false, true otherwise.
     */
    virtual bool removePIDForId(int id) = 0;

    /**
     * @brief ~IPIDTableManager Virtual destructor.
     */
    virtual ~IPIDTableManager() {}
};

#endif // IPIDTABLEMANAGER

