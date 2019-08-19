cmake_minimum_required(VERSION 2.8.3)
project(leo_navigation)

find_package(catkin)

catkin_package()

install(DIRECTORY launch/
    DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/launch
    PATTERN ".svn" EXCLUDE)

# catkin_install_python(PROGRAMS 
#     scripts/serial_bridge
#     scripts/leo_system
#     DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})