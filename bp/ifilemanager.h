#ifndef IFILEMANAGER
#define IFILEMANAGER

#include "file.h"

/**
 * @brief The IFileManager class works with database table files.
 */
class IFileManager {
public:

    /**
     * @brief getFileById Finds file with parameter id and if everything is OK fills file
     * as the second parameter. If any error occurs, given parameter file is not modified.
     * @param id Id of file which is to be searched.
     * @param file File which will be set according to data in database.
     * @return true is everything goes normally else false.
     */
    virtual bool getFileById(int id, File* file) = 0;

    /**
     * @brief ~IFileManager Virtual destructor.
     */
    virtual ~IFileManager() {}
};
#endif // IFILEMANAGER

