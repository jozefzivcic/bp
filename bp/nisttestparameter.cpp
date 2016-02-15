#include "nisttestparameter.h"
#include <iostream>
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

NistTestParameter &NistTestParameter::operator =(NistTestParameter other)
{
    swap(other);
    return *this;
}

void NistTestParameter::swap(NistTestParameter &par)
{
    using std::swap;
    swap(testId, par.testId);
    swap(length, par.length);
    swap(testNumber, par.testNumber);
    swap(streams, par.streams);
    swap(specialParameter, par.specialParameter);
    swap(containsStreams, par.containsStreams);
    swap(containsSpecialParameter, par.containsSpecialParameter);
}

bool NistTestParameter::getContainsStreams() const
{
    return containsStreams;
}

bool NistTestParameter::getContainsSpecialParameter() const
{
    return containsSpecialParameter;
}

NistTestParameter::NistTestParameter() : NistTestParameter(0,0,0) {}

NistTestParameter::NistTestParameter(long test, long l, int num):
    testId(test), length(l), testNumber(num), streams(1), specialParameter(0),
    containsStreams(false), containsSpecialParameter(false) {}

NistTestParameter::NistTestParameter(const NistTestParameter &par):
    testId(par.getTestId()), length(par.getLength()), testNumber(par.getTestNumber()),
    streams(par.getStreams()), specialParameter(par.getSpecialParameter()),
    containsStreams(par.containsStreams), containsSpecialParameter(par.containsSpecialParameter)
{}
