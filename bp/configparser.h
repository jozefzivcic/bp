#ifndef CONFIGPARSER_H
#define CONFIGPARSER_H
#include <iostream>
#include <map>

class ConfigParser
{
private:
    std::map<std::string, std::string> dictionary;
public:

    /**
     * @brief parseFile Loads all keys and their values.
     * @param file File, from which keys and values will be readed.
     * @return false if some error in config file structure occurs, true otherwise.
     */
    bool parseFile(std::string file);

    /**
     * @brief getValue Returns value associated with key.
     * @param key Key which will be searched in dictionary.
     * @return If key was found in dictionary, then associated value, if key was not
     * found in dictionary, then empty string.
     */
    std::string getValue(std::string key);

    /**
     * @brief reset Resets actual loaded config file.
     */
    void reset();
};

#endif // CONFIGPARSER_H
