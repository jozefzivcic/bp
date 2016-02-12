#include "configparser.h"
#include <fstream>

using namespace std;

bool ConfigParser::parseFile(string file)
{
    string line;
    ifstream fileStream(file);
    if (!fileStream.is_open())
        return false;
    string key;
    string value;
    size_t first, second, last;
    map<string,string> tempDictionary;
    while(getline(fileStream,line)) {
        if (line == "" || line[0] == '#')
            continue;
        if (line.length() < 6)
            return false;
        first = line.find('\"',0);
        if (first == string::npos || first + 1 >= line.length())
            return false;
        second = line.find('\"',first + 1);
        if (second == string::npos || second + 1 >= line.length() || line[second + 1] != '=')
            return false;
        if (first + 1 == second)
            return false;
        if (second + 2 >= line.length() || line[second + 2] != '\"')
            return false;
        if (second + 3 >= line.length())
            return false;
        last = line.find('\"', second + 3);
        if (last == string::npos || last == second + 3)
            return false;
        key = line.substr(first + 1, second - first - 1);
        value = line.substr(second + 3, last - second - 3);
        tempDictionary.insert(make_pair(key,value));
    }
    fileStream.close();
    dictionary.clear();
    dictionary.insert(tempDictionary.begin(),tempDictionary.end());
    return true;
}

string ConfigParser::getValue(string key) const
{
    map<string, string>::const_iterator it;
    it = dictionary.find(key);
    if (it == dictionary.end())
        return "";
    return it->second;
}

void ConfigParser::reset()
{
    dictionary.clear();
}
