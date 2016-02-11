#include "nistcmdparamscreator.h"
#include <sstream>

using namespace std;

NistCmdParamsCreator::NistCmdParamsCreator() : params("-fast"), testNumber(0) {}

string NistCmdParamsCreator::getCmdParams() const
{
    return params;
}

void NistCmdParamsCreator::resetParams()
{
    params = "-fast";
    testNumber = 0;
}

void NistCmdParamsCreator::setLength(long length)
{
    string temp = " -length ";
    temp += convertLongToString(length);
    params += temp;
}

void NistCmdParamsCreator::setFile(string file)
{
    string temp = " -file ";
    temp += file;
    params += temp;
}

void NistCmdParamsCreator::setStreams(long streams)
{
    string temp = " - streams ";
    temp += convertLongToString(streams);
    params += temp;
}

bool NistCmdParamsCreator::setTest(int test)
{
    if (test < 1 || test > 15)
        return false;
    testNumber = test;
    string option = " -tests ";
    string parameter = "";
    for (int i = 1; i <= 15; i++) {
        if (test == i)
            parameter += "1";
        else
            parameter += "0";
    }
    option += parameter;
    params += option;
    return true;
}

bool NistCmdParamsCreator::setSpecialParameter(long param)
{
    if (testNumber == 0)
        return false;
    string option = "";
    switch (testNumber) {
    case 2:
        option += " -blockfreqpar ";
        break;
    case 8:
        option += " -nonoverpar ";
        break;
    case 9:
        option += " -overpar ";
        break;
    case 11:
        option += " -approxpar ";
        break;
    case 14:
        option += " -serialpar ";
        break;
    case 15:
        option += " -linearpar ";
        break;
    default:
        return false;
    }
    option += convertLongToString(param);
    params += option;
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

