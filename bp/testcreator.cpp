#include "testcreator.h"
#include "constants.h"

TestCreator::TestCreator()
{

}

bool TestCreator::createTest(Test t)
{
    if (t.testTable() == Constants::NIST)
        return createNistTest(t);
}

bool TestCreator::createNistTest(Test t)
{

    return true;
}

