cmake_minimum_required(VERSION 3.0.2)
project(leo_navigation)

find_package(catkin REQUIRED COMPONENTS
  tf
  nav_msgs)

catkin_package(
  CATKIN_DEPENDS
    tf
    nav_msgs
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)

add_executable(odom2tf
  src/odom2tf.cpp
)

target_link_libraries(odom2tf
  ${catkin_LIBRARIES}
)

install(
  DIRECTORY
    config
    launch
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)

install(TARGETS firmware_message_converter
  RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

