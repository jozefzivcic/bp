QMAKE_CXXFLAGS += -std=c++11 -pedantic -Wall -Wextra
TEMPLATE = app
CONFIG += console c++11
CONFIG -= app_bundle
CONFIG -= qt
LIBS += -lmysqlcppconn -pthread
SOURCES += main.cpp \
    mysqlfilemanager.cpp \
    file.cpp \
    mysqltestmanager.cpp \
    test.cpp \
    mysqlcurrentlyrunningmanager.cpp \
    scheduler.cpp \
    queuecomparator.cpp \
    prioritycomparator.cpp \
    testhandler.cpp \
    threadhandler.cpp \
    testcreator.cpp \
    nistcmdparamscreator.cpp \
    configparser.cpp \
    configstorage.cpp \
    mainclass.cpp \
    nisttestparameter.cpp \
    mysqlnisttestsmanager.cpp \
    classtocmdparamconverter.cpp \
    linuxfilestructurehandler.cpp \
    logger.cpp \
    mysqlresultsmanager.cpp \
    mysqldbpool.cpp \
    mysqlpidtablemanager.cpp

HEADERS += \
    ifilemanager.h \
    file.h \
    mysqlfilemanager.h \
    itestmanager.h \
    mysqltestmanager.h \
    test.h \
    icurrentlyrunningmanager.h \
    mysqlcurrentlyrunningmanager.h \
    scheduler.h \
    ischeduler.h \
    queuecomparator.h \
    iprioritycomparator.h \
    prioritycomparator.h \
    itesthandler.h \
    testhandler.h \
    threadhandler.h \
    itestcreator.h \
    testcreator.h \
    nistcmdparamscreator.h \
    configparser.h \
    configstorage.h \
    mainclass.h \
    nisttestparameter.h \
    inisttestsmanager.h \
    mysqlnisttestsmanager.h \
    iclasstocmdparamconverter.h \
    classtocmdparamconverter.h \
    ifilestructurehandler.h \
    linuxfilestructurehandler.h \
    ilogger.h \
    logger.h \
    iresultsmanager.h \
    mysqlresultsmanager.h \
    generaldbpool.h \
    mysqldbpool.h \
    ipidtablemanager.h \
    mysqlpidtablemanager.h

