import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (DeclareLaunchArgument, EmitEvent, LogInfo,
                            RegisterEventHandler)
from launch.events import matches_action
from launch.substitutions import (LaunchConfiguration)
from launch_ros.actions import LifecycleNode
from launch_ros.event_handlers import OnStateTransition
from launch_ros.events.lifecycle import ChangeState
from lifecycle_msgs.msg import Transition


def generate_launch_description():
    params_file = LaunchConfiguration('params_file')
    scan_topic = LaunchConfiguration('scan_topic')

    declare_params_file_cmd = DeclareLaunchArgument(
        'params_file',
        default_value=os.path.join(get_package_share_directory("leo_nav"),
                                   'config', 'slam_toolbox.yaml'),
        description='Full path to the ROS2 parameters file to use for the slam_toolbox node')
    
    declare_scan_topic_cmd = DeclareLaunchArgument(
        'scan_topic',
        default_value='/scan',
        description='Topic for laser scan data')

    start_async_slam_toolbox_node = LifecycleNode(
        parameters=[
          params_file,
        ],
        remappings=[
            ('/scan', scan_topic),
        ],
        package='slam_toolbox',
        executable='async_slam_toolbox_node',
        name='slam_toolbox',
        output='screen',
        namespace=''
    )

    configure_event = EmitEvent(
        event=ChangeState(
          lifecycle_node_matcher=matches_action(start_async_slam_toolbox_node),
          transition_id=Transition.TRANSITION_CONFIGURE
        )
    )

    activate_event = RegisterEventHandler(
        OnStateTransition(
            target_lifecycle_node=start_async_slam_toolbox_node,
            start_state="configuring",
            goal_state="inactive",
            entities=[
                LogInfo(msg="[LifecycleLaunch] Slam Toolbox node is activating."),
                EmitEvent(event=ChangeState(
                    lifecycle_node_matcher=matches_action(start_async_slam_toolbox_node),
                    transition_id=Transition.TRANSITION_ACTIVATE
                ))
            ]
        )
    )

    ld = LaunchDescription()

    ld.add_action(declare_params_file_cmd)
    ld.add_action(declare_scan_topic_cmd)
    ld.add_action(start_async_slam_toolbox_node)
    ld.add_action(configure_event)
    ld.add_action(activate_event)

    return ld