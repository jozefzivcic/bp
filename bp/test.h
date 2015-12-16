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
    //bool _run;
    //bool _ended;
public:
    Test();
    Test(const Test& t);
    int id() const;
    void setId(int id);
    int idFile() const;
    void setIdFile(int idFile);
    int idUser() const;
    void setIdUser(int idUser);
    time_t timeOfAdd() const;
    void setTimeOfAdd(const time_t &timeOfAdd);
    std::string testTable() const;
    void setTestTable(const std::string &testTable);
    Test& operator =(Test other);
    friend std::ostream& operator <<(std::ostream& out, const Test& t);
private:
    void swap(Test& t);
};

#endif // TEST_H
