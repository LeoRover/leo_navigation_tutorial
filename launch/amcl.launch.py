import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (DeclareLaunchArgument, EmitEvent, LogInfo,
                            RegisterEventHandler)
from launch.events import matches_action
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import LifecycleNode
from launch_ros.event_handlers import OnStateTransition
from launch_ros.events.lifecycle import ChangeState
from lifecycle_msgs.msg import Transition


def generate_launch_description():
    params_file = LaunchConfiguration('params_file')
    map_file = LaunchConfiguration('map_file')
    scan_topic = LaunchConfiguration('scan_topic')

    declare_params_file_cmd = DeclareLaunchArgument(
        'params_file',
        default_value=os.path.join(get_package_share_directory("leo_nav"),
                                   'config', 'amcl.yaml'),
        description='Full path to the ROS2 parameters file to use for the AMCL node')
    
    declare_map_file_cmd = DeclareLaunchArgument(
        'map_file',
        default_value=os.path.join(get_package_share_directory("leo_nav"),
                                   'maps', 'empty_map.yaml'),
        description='Full path to the map YAML file to load (required for AMCL)',
    )

    declare_scan_topic_cmd = DeclareLaunchArgument(
        'scan_topic',
        default_value='/scan',
        description='Topic for laser scan data')

    start_amcl_node = LifecycleNode(
        parameters=[params_file],
        remappings=[
            ('/scan', scan_topic),
        ],
        package='nav2_amcl',
        executable='amcl',
        name='amcl_node',
        output='screen',
        namespace=''
    )

    start_map_server_node = LifecycleNode(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        namespace='',
        output='screen',
        parameters=[{'yaml_filename': map_file}]
    )

    configure_map_server = EmitEvent(
        event=ChangeState(
            lifecycle_node_matcher=matches_action(start_map_server_node),
            transition_id=Transition.TRANSITION_CONFIGURE
        )
    )

    activate_map_server = RegisterEventHandler(
        OnStateTransition(
            target_lifecycle_node=start_map_server_node,
            start_state='configuring',
            goal_state='inactive',
            entities=[
                LogInfo(msg='[LifecycleLaunch] Loading map via map_server.'),
                EmitEvent(
                    event=ChangeState(
                        lifecycle_node_matcher=matches_action(start_map_server_node),
                        transition_id=Transition.TRANSITION_ACTIVATE
                    )
                )
            ]
        )
    )

    configure_amcl = EmitEvent(
        event=ChangeState(
            lifecycle_node_matcher=matches_action(start_amcl_node),
            transition_id=Transition.TRANSITION_CONFIGURE
        )
    )

    activate_amcl = RegisterEventHandler(
        OnStateTransition(
            target_lifecycle_node=start_amcl_node,
            start_state='configuring',
            goal_state='inactive',
            entities=[
                LogInfo(msg='[LifecycleLaunch] Activating AMCL node.'),
                EmitEvent(
                    event=ChangeState(
                        lifecycle_node_matcher=matches_action(start_amcl_node),
                        transition_id=Transition.TRANSITION_ACTIVATE
                    )
                )
            ]
        )
    )

    ld = LaunchDescription()

    ld.add_action(declare_params_file_cmd)
    ld.add_action(declare_map_file_cmd)
    ld.add_action(declare_scan_topic_cmd)
    ld.add_action(start_amcl_node)
    ld.add_action(start_map_server_node)
    ld.add_action(configure_map_server)
    ld.add_action(activate_map_server)
    ld.add_action(configure_amcl)
    ld.add_action(activate_amcl)

    return ld
