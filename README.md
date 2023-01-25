# leo_navigation

This package was created as part of the [Autonomous Navigation tutorial] for Leo Rover. It provides configuration for SLAM and autonomous navigation for Leo Rover equipped with IMU and LiDAR sensors. 

## Launch files

* **`odometry.launch`** 
 
    Starts the `ekf_localization_node` from [robot_localization] which publishes the odometry based on Wheel encoders and IMU readings.

    **Arguments:**
    * `three_d` (default: `false`)
    
        If set to `true`, also starts [imu_filter_madgwick] to fuse data from IMU sensor into an orientation and uses it in the `ekf_localization_node` to provide a 3D odometry.

* **`gmapping.launch`**

    Starts the `slam_gmapping` node from [gmapping] package which provides a laser-based SLAM.

* **`amcl.launch`** 

    Starts [map_server] which publishes static map from a file on a ROS topic and [amcl] which uses odometry and data from the LiDAR sensor to estimate the localization of the robot on the map.

    **Arguments:**
    * `map_file` (**required**)

        An absolute path to the map file in the format supported by `map_server`.

* **`twist_mux.launch`**

    Starts [twist_mux] node which multiplexes several sources of velocity commands for the robot, giving priority to manual control over autonomous.

    **Arguments:**
    * `cmd_vel_out` (default: `cmd_vel`)

        The topic name the multiplexer should publish velocity commands on.

* **`move_base.launch`**

    Starts [move_base] node which, given the robot's localization, a map of obstacles, laser scans and a navigation goal, plans a safe path to the goal and tries to execute it, by sending velocity commands to the robot.

* **`navigation.launch`**

    Starts `twist_mux.launch` and `move_base.launch`.

[Autonomous Navigation tutorial]: https://docs.leorover.tech/development-tutorials/autonomous-navigation
[geometry_msgs/TwistWithCovarianceStamped]: http://docs.ros.org/en/api/geometry_msgs/html/msg/TwistWithCovarianceStamped.html
[sensor_msgs/Imu]: http://docs.ros.org/en/api/sensor_msgs/html/msg/Imu.html
[geometry_msgs/TwistStamped]: http://docs.ros.org/en/api/geometry_msgs/html/msg/TwistStamped.html
[geometry_msgs/Vector3Stamped]: http://docs.ros.org/en/api/geometry_msgs/html/msg/TwistWithCovarianceStamped.html
[leo_firmware]: https://github.com/LeoRover/leo_firmware
[robot_localization]: http://wiki.ros.org/robot_localization
[imu_filter_madgwick]: http://wiki.ros.org/imu_filter_madgwick
[gmapping]: http://wiki.ros.org/gmapping
[amcl]: http://wiki.ros.org/amcl
[map_server]: http://wiki.ros.org/map_server
[twist_mux]: http://wiki.ros.org/twist_mux
[move_base]: http://wiki.ros.org/move_base
