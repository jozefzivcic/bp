#include "configstorage.h"

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

std::string ConfigStorage::getPathToNistBinary() const
{
    return pathToNistBinary;
}

ConfigStorage::ConfigStorage(ConfigParser *parser):
    database(parser->getValue("DATABASE")), userName(parser->getValue("USERNAME")),
    userPassword(parser->getValue("USER_PASSWORD")), schema(parser->getValue("SCHEMA")),
    nist(parser->getValue("NIST")), pathToNistBinary(parser->getValue("PATH_TO_NIST_BINARY"))
{}

