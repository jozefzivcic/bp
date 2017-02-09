#include "nistcmdparamscreator.h"
#include "logger.h"
#include <sstream>
#include <cstring>

using namespace std;

NistCmdParamsCreator::NistCmdParamsCreator() : testNumber(0)
{
    logger = new Logger();
    prepareDefaultParams();
}

NistCmdParamsCreator::~NistCmdParamsCreator()
{
    if (logger != nullptr)
        delete logger;
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
    prepareDefaultParams();
    testNumber = 0;
}

void NistCmdParamsCreator::setBinary(string bin)
{
    params.push_front(bin);
}

void NistCmdParamsCreator::setLength(long length)
{
    params.push_back(convertLongToString(length));
}

void NistCmdParamsCreator::setFile(string file)
{
    string temp = "-file";
    params.push_back(temp);
    params.push_back(file);
}

void NistCmdParamsCreator::setStreams(long streams)
{
    string temp = "-streams";
    params.push_back(temp);
    params.push_back(convertLongToString(streams));
}

bool NistCmdParamsCreator::setTest(int test)
{
    if (test < 1 || test > 15)
        return false;
    testNumber = test;
    string option = "-tests";
    params.push_back(option);
    string parameter = "000000000000000";
    parameter[test - 1] = '1';
    params.push_back(parameter);
    return true;
}

bool NistCmdParamsCreator::setSpecialParameter(long param)
{
    if (testNumber == 0)
        return false;
    string option;
    switch (testNumber) {
    case 2:
        option += "-blockfreqpar";
        break;
    case 8:
        option += "-nonoverpar";
        break;
    case 9:
        option += "-overpar";
        break;
    case 11:
        option += "-approxpar";
        break;
    case 14:
        option += "-serialpar";
        break;
    case 15:
        option += "-linearpar";
        break;
    default:
        return false;
    }
    params.push_back(option);
    params.push_back(convertLongToString(param));
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

void NistCmdParamsCreator::prepareDefaultParams()
{
    params.clear();
    params.push_back("-fast");
    params.push_back("-binary");
    params.push_back("-fileoutput");
}
