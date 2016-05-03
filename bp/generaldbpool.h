#ifndef GENERALDBPOOL
#define GENERALDBPOOL
#include <iostream>
#include <list>
#include <mutex>
#include <thread>
#include <algorithm>
#include <atomic>
#include "ilogger.h"
#include "logger.h"
#include "map"
#include <utility>

template <typename T>
class GeneralDBPool {
private:

    /**
     * @brief cons Map of connections, key is connection, value is true or false.
     */
    std::map<T*, bool> cons;

    /**
     * @brief isReady If thread can be used already.
     */
    bool isReady = false;

    /**
     * @brief numOfCons Defines number of connections that are created with this class.
     */
    volatile int numOfCons = 0;

    /**
     * @brief conMutex Mutex for calling methods from more threads.
     */
    std::mutex conMutex;

    /**
     * @brief logger Logging class.
     */
    ILogger* logger = new Logger();
public:

    /**
     * @brief ~GeneralDBPool Destructor.
     */
    virtual ~GeneralDBPool() {
        if (logger != nullptr)
            delete logger;
    }

    /**
     * @brief createPool Creates new pool, this method is not thread safe.
     * @param num Number of connections to create.
     * @return If pool is already created of num is less than 1 false, true otherwise.
     */
    bool createPool(int num) {
        if (isReady || num < 1)
            return false;
        numOfCons = num;
        T* con;
        for (int i = 0; i < num; i++) {
            if ((con = createConnection()) == nullptr) {
                destroyPool();
                return false;
            }
            cons.insert(std::make_pair(con, true));
        }
        isReady = true;
        return true;
    }

    /**
     * @brief destroyPool Destroys connection pool.
     */
    void destroyPool() {
        isReady = false;
        typename std::map<T*, bool>::iterator iter;
        for (iter = cons.begin(); !cons.empty() && iter != cons.end(); iter++) {
            deleteConnection(iter->first);
        }
    }

    /**
     * @brief getConnectionFromPool Returns connection. This method is thread safe.
     * @return Connection that may be used or nullptr if no connection is available.
     */
    T* getConnectionFromPool() {
        std::unique_lock<std::mutex> lck(conMutex);
        if (!isReady)
            return nullptr;
        T* con = nullptr;
        typename std::map<T*, bool>::iterator iter;
        for (iter = cons.begin(); iter != cons.end(); iter++) {
            if (iter->second) {
                iter->second = false;
                con = iter->first;
                break;
            }
        }
        if (iter == cons.end())
            return nullptr;
        if (!pingConnection(con)) {
            deleteConnection(con);
            cons.erase(iter);
            con = createConnection();
            cons.insert(std::make_pair(con, false));
        }
        return con;
    }

    /**
     * @brief releaseConnection Returns connection back to pool.
     * @param con Connection to be returned.
     * @return If connection is nullptr then false, true otherwise.
     */
    bool releaseConnection(T* con) {
        std::unique_lock<std::mutex> lck(conMutex);
        if (con == nullptr)
            return false;
        typename std::map<T*,bool>::iterator iter = cons.find(con);
        if (iter == cons.end())
            return false;
        iter->second = true;
        return true;
    }
protected:
    /**
     * @brief createConnection Creates new concrete connection.
     * @return New Connection.
     */
    virtual T* createConnection() = 0;

    /**
     * @brief deleteConnection Deletes one concrete connection.
     * @param con Connection to delete.
     * @return False if con is nullptr, true otherwise.
     */
    virtual bool deleteConnection(T* con) = 0;

    /**
     * @brief pingConnection Ping database if connection can be used.
     * @param con Connection to ping.
     * @return False if connection is not available and can't be used, true if everything is OK.
     */
    virtual bool pingConnection(T* con) = 0;
};

#endif // GENERALDBPOOL
