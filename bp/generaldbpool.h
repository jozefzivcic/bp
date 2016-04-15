#ifndef GENERALDBPOOL
#define GENERALDBPOOL
#include <iostream>
#include <list>
#include <mutex>
#include <thread>
#include <algorithm>
#include "ilogger.h"
#include "logger.h"

template <typename T>
class GeneralDBPool {
private:
    std::list<T*> freeConnections;
    std::list<T*> usedConnections;
    bool isReady = false;
    int numOfCons = 0;
    std::mutex conMutex;
    std::mutex getMutex;
    ILogger* logger = new Logger();
public:

    virtual ~GeneralDBPool() {}

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
            freeConnections.push_back(con);
        }
        isReady = true;
        return true;
    }

    void destroyPool() {
        isReady = false;
        typename std::list<T*>::iterator iter;
        for (iter = freeConnections.begin(); iter != freeConnections.end(); iter++) {
            deleteConnection(*iter);
        }
        for (iter = usedConnections.begin(); iter != usedConnections.end(); iter++) {
            deleteConnection(*iter);
        }
    }

    T* getConnectionFromPool() {
        std::unique_lock<std::mutex> lck(conMutex);
        if (!isReady)
            return nullptr;
        T* con = nullptr;
        if (!freeConnections.empty()) {
            typename std::list<T*>::iterator iter;
            iter = freeConnections.begin();
            con = *iter;
            if (!pingConnection(con)) {
                deleteConnection(con);
                con = createConnection();
            }
            freeConnections.erase(iter);
            usedConnections.push_back(con);
        }
        return con;
    }

    T* getConnectionFromPoolBusy() {
        std::unique_lock<std::mutex> lck(getMutex);
        logger->logInfo("Entered getConnectionFromPoolBusy");
        if (!isReady)
            return nullptr;
        T* con = nullptr;
        while ((con = getConnectionFromPool()) == nullptr)
            std::this_thread::sleep_for(std::chrono::milliseconds(1));
        logger->logInfo("Leaved getConnectionFromPoolBusy");
        return con;
    }

    bool releaseConnection(T* con) {
        std::unique_lock<std::mutex> lck(conMutex);
        if (con == nullptr)
            return false;
        typename std::list<T*>::iterator iter;
        iter = std::find(usedConnections.begin(), usedConnections.end(), con);
        if (iter == usedConnections.end()) {
            return false;
        }
        usedConnections.erase(iter);
        freeConnections.push_back(con);
        return true;
    }
protected:
    virtual T* createConnection() = 0;

    virtual bool deleteConnection(T* con) = 0;

    virtual bool pingConnection(T* con) = 0;
};

#endif // GENERALDBPOOL

