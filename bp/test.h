#ifndef TEST_H
#define TEST_H
#include <iostream>
#include "itestparameter.h"
class Test
{
private:
    int _id;
    int _idFile;
    int _idUser;
    time_t _timeOfAdd;
    std::string _testTable;
    bool _run;
    bool _ended;
public:
    Test();
};

#endif // TEST_H
