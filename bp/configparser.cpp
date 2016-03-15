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
    size_t pos;
    bool isEscape;
    map<string,string> tempDictionary;
    while(getline(fileStream,line)) {
        if (line == "" || line[0] == '#')
            continue;
        if (line.length() < 3)
            return false;
        pos = 0;
        isEscape = false;
        while((pos = line.find('=', pos)) != string::npos) {
            if (pos > 0 && line[pos - 1] == '\\') {
                pos++;
                isEscape = true;
            }else if (pos > 0) {
                break;
            }
        }
        if (pos == string::npos)
            return false;
        key = line.substr(0, pos);
        value = line.substr(pos + 1, line.length() - pos - 1);
        if (isEscape) {
            key = eraseEscapeCharacters(key);
            value = eraseEscapeCharacters(value);
        }
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

string ConfigParser::eraseEscapeCharacters(string str)
{
    string::iterator iter = str.begin();
    while(iter != str.end()) {
        if (*iter == '\\' && (iter + 1) != str.end() && *(iter + 1) == '\\')
            iter++;
        else if (*iter == '\\')
            iter = str.erase(iter);
        else
            iter++;
    }
    return str;
}
