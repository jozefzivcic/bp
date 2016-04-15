#ifndef CONFIGSTORAGE_H
#define CONFIGSTORAGE_H
#include <iostream>
#include "configparser.h"
#include "ilogger.h"
/**
 * @brief The ConfigStorage class holds all constants from .config file.
 */
class ConfigStorage
{
private:
    std::string database;
    std::string userName;
    std::string userPassword;
    std::string schema;
    std::string nist;
    std::string pathToNist;
    std::string pathToTestsPool;
    std::string pathToUsersDir;
    std::string pathToUsersDirFromPool;
    std::string testsResults;
    std::string nameOfApplication;
    size_t sleepInSeconds;
    int pooledConnections;
    ILogger* logger = nullptr;
    int rerunTimes;
public:
    ConfigStorage(ConfigParser* parser);
    ~ConfigStorage();
    std::string getDatabase() const;
    std::string getUserName() const;
    std::string getUserPassword() const;
    std::string getSchema() const;
    std::string getNist() const;
    std::string getPathToNist() const;
    std::string getPathToTestsPool() const;
    std::string getPathToUsersDir() const;
    std::string getPathToUsersDirFromPool() const;
    std::string getTestsResults() const;
    std::string getNameOfApplication() const;
    size_t getSleepInSeconds() const;
    int getPooledConnections() const;
    int getRerunTimes() const;
};

#endif // CONFIGSTORAGE_H
