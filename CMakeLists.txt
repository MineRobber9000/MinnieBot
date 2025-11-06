cmake_minimum_required(VERSION 3.12)
project(Miniscript VERSION 1.6.2 LANGUAGES C CXX)

option(MINISCRIPT_BUILD_TESTING "Build unit test executable" OFF)
set(MINISCRIPT_CMD_NAME "miniscript" CACHE STRING
	"Specifies the command-line MiniScript executable filename")

set(MINISCRIPT_HEADERS
	MiniScript-cpp/MiniScript/Dictionary.h
	MiniScript-cpp/MiniScript/List.h
	MiniScript-cpp/MiniScript/MiniscriptErrors.h
	MiniScript-cpp/MiniScript/MiniscriptInterpreter.h
	MiniScript-cpp/MiniScript/MiniscriptIntrinsics.h
	MiniScript-cpp/MiniScript/MiniscriptKeywords.h
	MiniScript-cpp/MiniScript/MiniscriptLexer.h
	MiniScript-cpp/MiniScript/MiniscriptParser.h
	MiniScript-cpp/MiniScript/MiniscriptTAC.h
	MiniScript-cpp/MiniScript/MiniscriptTypes.h
	MiniScript-cpp/MiniScript/QA.h
	MiniScript-cpp/MiniScript/RefCountedStorage.h
	MiniScript-cpp/MiniScript/SimpleString.h
	MiniScript-cpp/MiniScript/SimpleVector.h
	MiniScript-cpp/MiniScript/SplitJoin.h
	MiniScript-cpp/MiniScript/UnicodeUtil.h
	MiniScript-cpp/MiniScript/UnitTest.h
)

set(MINICMD_HEADERS
	MiniScript-cpp/DateTimeUtils.h
	MiniScript-cpp/OstreamSupport.h
	MiniScript-cpp/ShellIntrinsics.h
	MiniScript-cpp/editline/editline.h
	MiniScript-cpp/editline/unix.h
	MiniScript-cpp/whereami/whereami.h
)

add_library(miniscript-cpp
	MiniScript-cpp/MiniScript/Dictionary.cpp
	MiniScript-cpp/MiniScript/List.cpp
	MiniScript-cpp/MiniScript/MiniscriptInterpreter.cpp
	MiniScript-cpp/MiniScript/MiniscriptIntrinsics.cpp
	MiniScript-cpp/MiniScript/MiniscriptKeywords.cpp
	MiniScript-cpp/MiniScript/MiniscriptLexer.cpp
	MiniScript-cpp/MiniScript/MiniscriptParser.cpp
	MiniScript-cpp/MiniScript/MiniscriptTAC.cpp
	MiniScript-cpp/MiniScript/MiniscriptTypes.cpp
	MiniScript-cpp/MiniScript/QA.cpp
	MiniScript-cpp/MiniScript/SimpleString.cpp
	MiniScript-cpp/MiniScript/SimpleVector.cpp
	MiniScript-cpp/MiniScript/SplitJoin.cpp
	MiniScript-cpp/MiniScript/UnicodeUtil.cpp
	MiniScript-cpp/MiniScript/UnitTest.cpp
	${MINISCRIPT_HEADERS}
)

target_include_directories(miniscript-cpp PUBLIC MiniScript-cpp/MiniScript)

if(NOT WIN32)
	set(EDITLINE_SRC
		MiniScript-cpp/editline/complete.c
		MiniScript-cpp/editline/editline.c
		MiniScript-cpp/editline/sysunix.c
	)
endif()

add_executable(minicmd
	MiniScript-cpp/main.cpp
	MiniScript-cpp/DateTimeUtils.cpp
	MiniScript-cpp/OstreamSupport.cpp
	MiniScript-cpp/ShellIntrinsics.cpp
	MiniScript-cpp/whereami/whereami.c
	${EDITLINE_SRC}
	${MINICMD_HEADERS}
)
target_include_directories(minicmd PRIVATE MiniScript-cpp/editline)
target_link_libraries(minicmd PRIVATE miniscript-cpp)

set_target_properties(miniscript-cpp minicmd PROPERTIES
	CXX_STANDARD 14
	CXX_STANDARD_REQUIRED ON)
set_target_properties(minicmd PROPERTIES OUTPUT_NAME ${MINISCRIPT_CMD_NAME})

if(MINISCRIPT_BUILD_TESTING)
	enable_testing()
	add_custom_target(TestSuite SOURCES TestSuite.txt)
	add_executable(tests-cpp MiniScript-cpp/MiniScript/UnitTest.cpp)
	target_compile_definitions(tests-cpp PRIVATE UNIT_TEST_MAIN)
	target_link_libraries(tests-cpp PRIVATE miniscript-cpp)
	add_test(NAME Miniscript.cpp.UnitTests COMMAND tests-cpp)
	add_test(NAME Miniscript.cpp.Integration COMMAND minicmd --itest ${CMAKE_SOURCE_DIR}/TestSuite.txt)
	set_tests_properties(Miniscript.cpp.UnitTests Miniscript.cpp.Integration PROPERTIES FAIL_REGULAR_EXPRESSION "FAIL|Error")
endif()

install(TARGETS miniscript-cpp minicmd)
