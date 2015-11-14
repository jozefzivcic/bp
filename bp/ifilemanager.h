#ifndef IFILEMANAGER
#define IFILEMANAGER

#include "file.h"
class IFileManager {
public:
    virtual File getFileById(int id) const = 0;
    virtual ~IFileManager() {}
};
#endif // IFILEMANAGER

