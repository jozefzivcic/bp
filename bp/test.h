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
    int id;
    int fileId;
    int userId;
    time_t timeOfAdd;
    std::string testTable;
public:
    Test();
    Test(const Test& t);

    /* ---- Getters and setters ---- */
    int getId() const;
    void setId(int value);

    int getFileId() const;
    void setFileId(int value);

    int getUserId() const;
    void setUserId(int value);

    time_t getTimeOfAdd() const;
    void setTimeOfAdd(const time_t &value);

    std::string getTestTable() const;
    void setTestTable(const std::string &value);

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
