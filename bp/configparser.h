#ifndef CONFIGPARSER_H
#define CONFIGPARSER_H
#include <iostream>
#include <map>

/**
 * @brief The ConfigParser class This class is used to parse files with format key=value,
 * comments must begin with # as first character on the line. Escape character is \.
 */
class ConfigParser
{
private:

    /**
     * @brief dictionary Contains loaded keys and values from parsed file.
     */
    std::map<std::string, std::string> dictionary;
public:

    /**
     * @brief parseFile Loads all keys and their values. If an error occurs during parsing,
     * loaded content is not changed.
     * @param file File, from which keys and values will be read.
     * @return false if given file does not exists or if some error occurs in config file
     * structure, true otherwise.
     */
    bool parseFile(std::string file);

    /**
     * @brief getValue Returns value associated with key.
     * @param key Key which will be searched in a dictionary.
     * @return If key was found in dictionary, then associated value, if key was not
     * found in dictionary, then empty string.
     */
    std::string getValue(std::string key) const;

    /**
     * @brief reset Resets actual loaded config file.
     */
    void reset();

private:
    /**
     * @brief eraseEscapeCharacters Removes escape characters from given string.
     * @param str String, from which escape characters are removed.
     * @return String without escape characters.
     */
    std::string eraseEscapeCharacters(std::string str);
};

#endif // CONFIGPARSER_H
