#ifndef ICHANGESTATEMANAGER
#define ICHANGESTATEMANAGER

class IChangeStateManager {
public:
    /**
     * @brief getDBState Returns state of database.
     * @param state Variable, which is filled with database state. If an error occurs this variable
     * is not changed.
     * @return If an error occurs false, true otherwise.
     */
    virtual bool getDBState(int& state) = 0;

    /**
     * @brief ~IChangeStateManager Virtual destructor.
     */
    virtual ~IChangeStateManager() {}
};

#endif // ICHANGESTATEMANAGER

