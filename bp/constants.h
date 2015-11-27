#ifndef CONSTANTS
#define CONSTANTS
#include <iostream>
class Constants {
public:
    /**
     * @brief DATABASE Connection to database.
     */
    static const std::string DATABASE;

    /**
     * @brief USERNAME Name of user which will be logged in database.
     */
    static const std::string USERNAME;

    /**
     * @brief USER_PASSWORD Password of logged user.
     */
    static const std::string USER_PASSWORD;

    /**
     * @brief SCHEMA Database schema which contains tables for this programm.
     */
    static const std::string SCHEMA;
};

#endif // CONSTANTS

