#include "nisttestparameter.h"

long NistTestParameter::getTestId() const
{
    return testId;
}

long NistTestParameter::getLength() const
{
    return length;
}

int NistTestParameter::getTestNumber() const
{
    return testNumber;
}

long NistTestParameter::getStreams() const
{
    if (containsStreams)
        return streams;
    return 1;
}

void NistTestParameter::setStreams(long value)
{
    containsStreams = true;
    streams = value;
}

long NistTestParameter::getSpecialParameter() const
{
    if (containsSpecialParameter)
        return specialParameter;
    switch(testId) {
    case 2:
        return 128;
    case 8:
        return 9;
    case 9:
        return 9;
    case 11:
        return 10;
    case 14:
        return 16;
    case 15:
        return 500;
    default:
        return 0;
    }
}

void NistTestParameter::setSpecialParameter(long value)
{
    containsSpecialParameter = true;
    specialParameter = value;
}

NistTestParameter::NistTestParameter(long test, long l, int num):
    testId(test), length(l), testNumber(num), streams(1), specialParameter(0),
    containsStreams(false), containsSpecialParameter(false) {}
