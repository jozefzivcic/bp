#ifndef ICLASSTOCMDPARAMCONVERTER
#define ICLASSTOCMDPARAMCONVERTER
#include "nisttestparameter.h"
#include "test.h"
#include <iostream>

/**
 * @brief The IClassToCmdParamConverter class This class is used to convert parameters into
 * 2D array.
 */
class IClassToCmdParamConverter {
public:

    /**
     * @brief convertNistTestToArray Converts nist test and its parameter, which takes from
     * database, into 2D array, which can be used in execv function.
     * @param ptr Pointer to 2D array, which will be filled with arguments for a new program.
     * Memory needed is allocated into this pointer.
     * @param binary Name of binary to be executed.
     * @param t Test, with which is ptr filled.
     * @return If test table of test is not nist, or ptr is nullptr, or an error occurs,
     * then false. True otherwise.
     */
    virtual bool convertNistTestToArray(char*** ptr, std::string binary, Test t) = 0;

    /**
     * @brief convertNistTestToArray Converts nist test and its parameter into 2D array,
     * which can be used in execv function.
     * @param ptr Pointer to 2D array, which will be filled with arguments for a new program.
     * Memory needed is allocated into this pointer.
     * @param binary Name of binary to be executed.
     * @param t Test, with which is ptr filled.
     * @param param NistTestParameter, with which is ptr filled.
     * @return If test table of test is not nist, or ptr is nullptr, or an error occurs,
     * then false. True otherwise.
     */
    virtual bool convertNistTestToArray(char*** ptr, std::string binary, Test t, NistTestParameter param) = 0;

    /**
     * @brief deleteAllocatedArray Frees pointer filled with one of convert* methods.
     * @param ptr Pointer to be filled.
     * @return If ptr to 2D array, or 2D array is a nullptr then false, true otherwise.
     */
    virtual bool deleteAllocatedArray(char*** ptr) = 0;

    /**
     * @brief ~IClassToCmdParamConverter Virtual destructor.
     */
    virtual ~IClassToCmdParamConverter() {}
};

#endif // ICLASSTOCMDPARAMCONVERTER

