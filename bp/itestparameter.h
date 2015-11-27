#ifndef ITESTPARAMETER
#define ITESTPARAMETER

template <typename T>
class ITestParameter {
public:
    typedef T ValueType;
    virtual ValueType getParam() const = 0;
    //setParam(ValueType param) = 0;
};

#endif // ITESTPARAMETER

