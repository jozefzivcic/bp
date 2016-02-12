#ifndef CONFIGSTORAGE_H
#define CONFIGSTORAGE_H
#include <iostream>
#include "configparser.h"

class ConfigStorage
{
private:
    std::string database;
    std::string userName;
    std::string userPassword;
    std::string schema;
    std::string nist;
    std::string pathToNistBinary;
public:
    ConfigStorage(ConfigParser* parser);
    std::string getDatabase() const;
    std::string getUserName() const;
    std::string getUserPassword() const;
    std::string getSchema() const;
    std::string getNist() const;
    std::string getPathToNistBinary() const;
};

#endif // CONFIGSTORAGE_H
