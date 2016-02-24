#ifndef TEST_H
#define TEST_H
#include <iostream>
#include "itestparameter.h"

/**
 * @brief The Test class represents a record in database table tests.
 */
class Test
{
private:
    int _id;
    int _idFile;
    int _idUser;
    time_t _timeOfAdd;
    std::string _testTable;
public:
    Test();
    Test(const Test& t);
    /* ---- Getters and setters ---- */
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

    /**
     * @brief swap Swaps attributes with test t. This is used for copy-and-swap idiom.
     * @param t Test which attributes are swapped.
     */
    void swap(Test& t);
};

#endif // TEST_H
