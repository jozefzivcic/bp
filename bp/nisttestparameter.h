#ifndef NISTTESTPARAMETER_H
#define NISTTESTPARAMETER_H


class NistTestParameter
{
private:
    long testId;
    long length;
    int testNumber;
    long streams;
    long specialParameter;
    bool containsStreams;
    bool containsSpecialParameter;
public:
    NistTestParameter(long test, long l, int num);
    long getTestId() const;
    long getLength() const;
    int getTestNumber() const;
    long getStreams() const;
    void setStreams(long value);
    long getSpecialParameter() const;
    void setSpecialParameter(long value);
};

#endif // NISTTESTPARAMETER_H
