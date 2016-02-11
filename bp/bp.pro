QMAKE_CXXFLAGS += -std=c++11 -pedantic -Wall -Wextra
TEMPLATE = app
CONFIG += console c++11
CONFIG -= app_bundle
CONFIG -= qt
LIBS += -lmysqlcppconn -pthread
SOURCES += main.cpp \
    mysqlfilemanager.cpp \
    file.cpp \
    constants.cpp \
    mysqltestmanager.cpp \
    test.cpp \
    mysqlcurrentlyrunningmanager.cpp \
    scheduler.cpp \
    queuecomparator.cpp \
    prioritycomparator.cpp \
    mysqlchangestatemanager.cpp \
    testhandler.cpp \
    threadhandler.cpp \
    testcreator.cpp \
    nistcmdparamscreator.cpp

HEADERS += \
    ifilemanager.h \
    file.h \
    constants.h \
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
    ichangestatemanager.h \
    mysqlchangestatemanager.h \
    itesthandler.h \
    testhandler.h \
    threadhandler.h \
    itestcreator.h \
    testcreator.h \
    nistcmdparamscreator.h

