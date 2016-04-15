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
    std::map<T*, bool> cons;
    bool isReady = false;
    volatile int numOfCons = 0;
    std::mutex conMutex;
    ILogger* logger = new Logger();
public:

    virtual ~GeneralDBPool() {
        if (logger != nullptr)
            delete logger;
    }

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

    void destroyPool() {
        isReady = false;
        typename std::map<T*, bool>::iterator iter;
        for (iter = cons.begin(); !cons.empty() && iter != cons.end(); iter++) {
            deleteConnection(iter->first);
        }
    }

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
    virtual T* createConnection() = 0;

    virtual bool deleteConnection(T* con) = 0;

    virtual bool pingConnection(T* con) = 0;
};

#endif // GENERALDBPOOL
