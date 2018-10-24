cmake_minimum_required(VERSION 2.8.3)
project(jaco_manipulation_test)
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

set(COMPILER "UNKNOWN")

if(CMAKE_COMPILER_IS_GNUCXX)
  set(COMPILER "G")
elseif(CMAKE_CXX_COMPILER_ID MATCHES "AppleClang")
  set(COMPILER "Apple Clang")
elseif(CMAKE_CXX_COMPILER_ID MATCHES "AppleClang")
  set(COMPILER "Clang")
endif()

if("${COMPILER}" STREQUAL "UNKNOWN")
  message(FATAL_ERROR "Invalid Compiler")
endif()

message(STATUS "${COMPILER}++ Version : " ${CMAKE_CXX_COMPILER_VERSION})
message(STATUS "${COMPILER}++ Location: " ${CMAKE_CXX_COMPILER})

### Require out-of-source builds
file(TO_CMAKE_PATH "${PROJECT_BINARY_DIR}/CMakeLists.txt" LOC_PATH)
if(EXISTS "${LOC_PATH}")
  message(FATAL_ERROR "You cannot build in a source directory (or any directory with a CMakeLists.txt file). Please make a build subdirectory. Feel free to remove CMakeCache.txt and CMakeFiles.")
endif()

catkin_python_setup()

find_package(catkin REQUIRED COMPONENTS
             anchor_msgs
             cmake_modules
             jaco_manipulation
             roscpp
             rospy)

find_package(Boost REQUIRED)

catkin_package(
    INCLUDE_DIRS include
    CATKIN_DEPENDS jaco_manipulation anchor_msgs roscpp rospy cmake_modules)

# TESTS

add_library(csv_reader src/csv_reader.cpp)
add_dependencies(csv_reader ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})
target_include_directories(csv_reader PUBLIC include ${Boost_INCLUDE_DIRS} ${catkin_INCLUDE_DIRS})
target_link_libraries(csv_reader
                      ${catkin_LIBRARIES}
                      ${Boost_LIBRARIES})

# Test client for jaco_manipulation action server
add_executable(client_test src/client_test.cpp)
add_dependencies(client_test ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})
target_include_directories(client_test PUBLIC include ${catkin_INCLUDE_DIRS})
target_link_libraries(client_test
                      ${catkin_LIBRARIES})

# Test client for jaco_manipulation grasping
add_executable(client_grasp_test src/client_grasp_test.cpp)
add_dependencies(client_grasp_test ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})
target_include_directories(client_grasp_test PUBLIC include ${catkin_INCLUDE_DIRS})
target_link_libraries(client_grasp_test
                      ${catkin_LIBRARIES}
                      jaco2_manipulation)
# Baseline test
add_executable(baseline_test src/baseline_test.cpp src/baseline_csv_reader.cpp)
add_dependencies(baseline_test ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})
target_include_directories(baseline_test PUBLIC include ${catkin_INCLUDE_DIRS})
target_link_libraries(baseline_test
                      ${catkin_LIBRARIES}
                      csv_reader)
# anchoring test
add_executable(anchoring_test src/run_anchoring_test.cpp src/anchoring_test.cpp src/anchoring_base_test.cpp src/baseline_csv_reader.cpp)
add_dependencies(anchoring_test ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})
target_include_directories(anchoring_test PUBLIC include ${catkin_INCLUDE_DIRS})
target_link_libraries(anchoring_test
                      ${catkin_LIBRARIES}
                      csv_reader)

# edge case anchoring test
add_executable(anchoring_edge_case_test src/run_anchoring_edge_case_test.cpp src/anchoring_edge_case_test.cpp src/anchoring_base_test.cpp src/baseline_csv_reader.cpp)
add_dependencies(anchoring_edge_case_test ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})
target_include_directories(anchoring_edge_case_test PUBLIC include ${catkin_INCLUDE_DIRS})
target_link_libraries(anchoring_edge_case_test
                      ${catkin_LIBRARIES}
                      csv_reader)

# obstacle anchoring test
add_executable(obstacle_anchoring_test src/run_obstacle_anchoring_test.cpp src/obstacle_anchoring_test.cpp src/anchoring_base_test.cpp src/baseline_csv_reader.cpp)
add_dependencies(obstacle_anchoring_test ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})
target_include_directories(obstacle_anchoring_test PUBLIC include ${catkin_INCLUDE_DIRS})
target_link_libraries(obstacle_anchoring_test
                      ${catkin_LIBRARIES}
                      csv_reader)
