#ifndef CONFIGSTORAGE_H
#define CONFIGSTORAGE_H
#include <iostream>
#include "configparser.h"

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
public:
    ConfigStorage(ConfigParser* parser);
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
};

#endif // CONFIGSTORAGE_H
