#ifndef NISTTESTPARAMETER_H
#define NISTTESTPARAMETER_H

/**
 * @brief The NistTestParameter class represents a record in database table nist_tests.
 */
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
    /**
     * @brief NistTestParameter Constructor.
     */
    NistTestParameter();

    /**
     * @brief NistTestParameter Constructor.
     * @param test Test id.
     * @param l Length - number of bits for testing.
     * @param num testNumber - which test to execute.
     */
    NistTestParameter(long test, long l, int num);

    /**
     * @brief NistTestParameter Copy constructor.
     * @param par Another NistTestParameter, which attribute values will be setted into new
     * creating class.
     */
    NistTestParameter(const NistTestParameter& par);
    NistTestParameter& operator =(NistTestParameter other);
    /*-------- getters and setters --------*/
    long getTestId() const;
    long getLength() const;
    int getTestNumber() const;
    long getStreams() const;
    void setStreams(long value);
    long getSpecialParameter() const;
    void setSpecialParameter(long value);
    bool getContainsStreams() const;
    bool getContainsSpecialParameter() const;
private:

    /**
     * @brief swap Used for copy-and-swap idiom. Swaps attributes with NistTestParameter par.
     * @param par Parameter with which are attributes swapped.
     */
    void swap(NistTestParameter& par);
};

#endif // NISTTESTPARAMETER_H
