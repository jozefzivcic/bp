#include "configstorage.h"
#include <stdexcept>
#include <logger.h>
#include <string>

using namespace std;

std::string ConfigStorage::getDatabase() const
{
    return database;
}

std::string ConfigStorage::getUserName() const
{
    return userName;
}

std::string ConfigStorage::getUserPassword() const
{
    return userPassword;
}

std::string ConfigStorage::getSchema() const
{
    return schema;
}

std::string ConfigStorage::getNist() const
{
    return nist;
}

std::string ConfigStorage::getPathToNist() const
{
    return pathToNist;
}

std::string ConfigStorage::getPathToTestsPool() const
{
    return pathToTestsPool;
}

std::string ConfigStorage::getPathToUsersDir() const
{
    return pathToUsersDir;
}

std::string ConfigStorage::getPathToUsersDirFromPool() const
{
    return pathToUsersDirFromPool;
}

std::string ConfigStorage::getTestsResults() const
{
    return testsResults;
}

std::string ConfigStorage::getNameOfApplication() const
{
    return nameOfApplication;
}

size_t ConfigStorage::getSleepInSeconds() const
{
    return sleepInSeconds;
}

int ConfigStorage::getPooledConnections() const
{
    return pooledConnections;
}

int ConfigStorage::getRerunTimes() const
{
    return rerunTimes;
}

unsigned int ConfigStorage::getRerunAfter() const
{
    return rerunAfter;
}

ConfigStorage::ConfigStorage(ConfigParser *parser):
    database(parser->getValue("DATABASE")), userName(parser->getValue("USERNAME")),
    userPassword(parser->getValue("USER_PASSWORD")), schema(parser->getValue("SCHEMA")),
    nist(parser->getValue("NIST")), pathToNist(parser->getValue("PATH_TO_NIST")),
    pathToTestsPool(parser->getValue("PATH_TO_TESTS_POOL")),
    pathToUsersDir(parser->getValue("PATH_TO_USERS_DIR")),
    pathToUsersDirFromPool(parser->getValue("PATH_TO_USERS_DIR_FROM_POOL")),
    testsResults(parser->getValue("TESTS_RESULTS")),
    nameOfApplication(parser->getValue("NAME_OF_APPLICATION")),
    rerunTimes(stoi(parser->getValue("RERUN_TIMES"))),
    rerunAfter(stoi(parser->getValue("RERUN_TEST_IN_SEC")))
{
    logger = new Logger();
    try {
        sleepInSeconds = stoi(parser->getValue("SLEEP_IN_SECONDS"));
    }catch(invalid_argument& ex) {
        logger->logError("Wrong format of SLEEP_IN_SECONDS");
        throw;
    }
    try {
        pooledConnections = stoi(parser->getValue("POOLED_CONNECTIONS"));
    }catch(invalid_argument& ex) {
        logger->logError("Wrong format of POOLED_CONNECTIONS");
        throw;
    }
}

ConfigStorage::~ConfigStorage()
{
    if (logger != nullptr)
        delete logger;
}

