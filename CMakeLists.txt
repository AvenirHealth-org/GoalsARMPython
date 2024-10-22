cmake_minimum_required(VERSION 3.15...3.27)
project(${SKBUILD_PROJECT_NAME} LANGUAGES CXX)

message(STATUS ${SKBUILD_PROJECT_NAME})

set(PYBIND11_NEWPYTHON ON)
find_package(pybind11 CONFIG REQUIRED)

pybind11_add_module(goals_proj src/goals_proj/goals_proj.cpp)
target_compile_features(goals_proj PRIVATE cxx_std_20)

include(FetchContent)
message(CHECK_START "Locating GoalsARM C++")
list(APPEND CMAKE_MESSAGE_INDENT "  ")

set(GOALS_ARM_PATH "Path to local GoalsARM C++ library" CACHE STRING "")

## Stop GoalsARM building tests
option(BUILD_TESTING "" OFF)
include(CTest)

if(DEFINED ENV{LOCAL_BUILD} AND "$ENV{LOCAL_BUILD}" STREQUAL "true")

  if(EXISTS ${GOALS_ARM_PATH})
      message(STATUS "Local build enabled, using GoalsARM path: ${GOALS_ARM_PATH}")

      FetchContent_Declare(
        goals_arm
        SOURCE_DIR ${GOALS_ARM_PATH}
      )
  else()
    message(FATAL_ERROR "Error: LOCAL_BUILD is true, but path to GoalsARM '${GOALS_ARM_PATH}' does not exist.")
  endif()

else()

  # In non-local mode, check for GOALS_ARM_GIT_TAG or default to "main"
  set(GOALS_ARM_GIT_TAG "GoalsARM git tag to pull" CACHE STRING "main")
  message(STATUS "Pulling GoalsARM from git with tag: '${GOALS_ARM_GIT_TAG}'")

  FetchContent_Declare(
    goals_arm
    GIT_REPOSITORY https://github.com/AvenirHealth-org/GoalsARM.git
    GIT_TAG ${GOALS_ARM_GIT_TAG}
  )
endif()

FetchContent_MakeAvailable(goals_arm)
list(POP_BACK CMAKE_MESSAGE_INDENT)
message(CHECK_PASS "GoalsARM located")
target_include_directories(goals_proj PRIVATE ${goals_arm_SOURCE_DIR}/include)

# Ideally pulling in GoalsARM which has its own CMakeLists with Boost included
# would mean that we wouldn't need to declare this again here. But that is not
# working on windows, I think something I am not understanding with defining
# GoalsARM as header only library and how CMake resolves dependencies. But
# this works fine for now.
if(POLICY CMP0167)
   # This policy removes FindBoost module
   # in favour of using BoostConfig.cmake files
   # but it cannot locate these as reliably, so let's
   # just use the old policy for now.
   cmake_policy(SET CMP0167 OLD)
endif()
find_package(Boost 1.82 REQUIRED)
target_include_directories(goals_proj PRIVATE ${Boost_INCLUDE_DIRS})

install(TARGETS goals_proj LIBRARY DESTINATION .)
