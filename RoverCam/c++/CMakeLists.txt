cmake_minimum_required(VERSION 3.10)

project(RoverCam)

find_package( OpenCV REQUIRED )

include_directories("${PROJECT_SOURCE_DIR}")

# file(GLOB SOURCES "*.cpp")

add_executable(server server.cpp)
add_executable(client client.cpp)

SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -pthread")

target_link_libraries(server ${OpenCV_LIBS})
target_link_libraries(client ${OpenCV_LIBS})