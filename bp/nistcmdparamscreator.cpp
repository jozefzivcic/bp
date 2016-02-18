#include "nistcmdparamscreator.h"
#include <sstream>
#include <cstring>

using namespace std;

NistCmdParamsCreator::NistCmdParamsCreator() : testNumber(0)
{
    params.clear();
    params.push_back("-fast");
}

string NistCmdParamsCreator::getCmdParams() const
{
    string tempString;
    list<string>::const_iterator it;
    for (it = params.begin(); it != params.end(); it++) {
        tempString += *it;
        tempString += " ";
    }
    return tempString.substr(0, tempString.length() - 1);
}

void NistCmdParamsCreator::resetParams()
{
    params.clear();
    params.push_back("-fast");
    testNumber = 0;
}

void NistCmdParamsCreator::setBinary(string bin)
{
    params.push_front(bin);
}

void NistCmdParamsCreator::setLength(long length)
{
    string temp = "-length ";
    temp += convertLongToString(length);
    params.push_back(temp);
}

void NistCmdParamsCreator::setFile(string file)
{
    string temp = "-file ";
    temp += file;
    params.push_back(temp);
}

void NistCmdParamsCreator::setStreams(long streams)
{
    string temp = "-streams ";
    temp += convertLongToString(streams);
    params.push_back(temp);
}

bool NistCmdParamsCreator::setTest(int test)
{
    if (test < 1 || test > 15)
        return false;
    testNumber = test;
    string option = "-tests ";
    string parameter = "";
    for (int i = 1; i <= 15; i++) {
        if (test == i)
            parameter += "1";
        else
            parameter += "0";
    }
    option += parameter;
    params.push_back(option);
    return true;
}

bool NistCmdParamsCreator::setSpecialParameter(long param)
{
    if (testNumber == 0)
        return false;
    string option;
    switch (testNumber) {
    case 2:
        option += "-blockfreqpar ";
        break;
    case 8:
        option += "-nonoverpar ";
        break;
    case 9:
        option += "-overpar ";
        break;
    case 11:
        option += "-approxpar ";
        break;
    case 14:
        option += "-serialpar ";
        break;
    case 15:
        option += "-linearpar ";
        break;
    default:
        return false;
    }
    option += convertLongToString(param);
    params.push_back(option);
    return true;
}

bool NistCmdParamsCreator::fillArrayOfArguments(char ***ptr)
{
    if (ptr == nullptr)
        return false;
    *ptr = new char*[params.size() + 1];
    list<string>::const_iterator it;
    int i = 0;
    for (it = params.begin(); it != params.end(); it++) {
        (*ptr)[i] = new char[(*it).length() + 1];
        strcpy((*ptr)[i],(*it).c_str());
        i++;
    }
    (*ptr)[i] = NULL;
    return true;
}

bool NistCmdParamsCreator::deleteArrayOfArguments(char ***ptr)
{
    if (ptr == nullptr || *ptr == nullptr)
        return false;
    int i = 0;
    while((*ptr)[i] != NULL) {
        delete[] (*ptr)[i];
        i++;
    }
    delete[] (*ptr);
    (*ptr) = nullptr;
    return true;
}

string NistCmdParamsCreator::convertLongToString(long n)
{
    string number;
    stringstream strstream;
    strstream << n;
    strstream >> number;
    return number;
}
