#ifndef GENERALDBPOOL
#define GENERALDBPOOL

template <typename T>
class GeneralDBPool {
public:

    bool createPool(int num) {

    }

    void destroyPool() {

    }

    T* getConnectionFromPool() {

    }

    bool releaseConnection(T* con) {

    }

    virtual T* createConnection() = 0;

    virtual bool deleteConnection(T* con) = 0;
};

#endif // GENERALDBPOOL

