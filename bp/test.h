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
    long id;
    long fileId;
    long userId;
    time_t timeOfAdd;
    std::string testTable;
    time_t timeOfRerun;
    int numOfRuns;
    int returnValue;

public:
    Test();
    Test(const Test& t);

    /* ---- Getters and setters ---- */
    long getId() const;
    void setId(long value);

    long getFileId() const;
    void setFileId(long value);

    long getUserId() const;
    void setUserId(long value);

    time_t getTimeOfAdd() const;
    void setTimeOfAdd(const time_t &value);

    std::string getTestTable() const;
    void setTestTable(const std::string &value);

    time_t getTimeOfRerun() const;
    void setTimeOfRerun(const time_t &value);

    int getNumOfRuns() const;
    void setNumOfRuns(int value);

    int getReturnValue() const;
    void setReturnValue(int value);

    void increaseRuns();

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
