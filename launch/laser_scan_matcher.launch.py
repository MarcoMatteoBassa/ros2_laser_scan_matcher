from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument, TimerAction
from launch.actions import ExecuteProcess
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    # Declare launch arguments
    use_sim_time = LaunchConfiguration("use_sim_time", default="false")

    # Get the package share directory
    pkg_dir = get_package_share_directory("ros2_laser_scan_matcher")
    config_file = os.path.join(pkg_dir, "config", "laser_scan_matcher.yaml")
    config_file = (
        "/home/user/ros2_ws/src/ros2_laser_scan_matcher/config/laser_scan_matcher.yaml"
    )

    # Define the laser scan matcher node
    laser_scan_matcher_node = Node(
        package="ros2_laser_scan_matcher",
        executable="laser_scan_matcher",
        name="custom_laser_scan_matcher",
        output="screen",
        parameters=[config_file],
    )

    # Define the service call to enable laser odometry
    enable_laser_odom = ExecuteProcess(
        cmd=[
            "ros2",
            "service",
            "call",
            "/custom_laser_scan_matcher/custom_enable_laser_odom",
            "std_srvs/srv/SetBool",
            '{"data": true}',
        ],
        output="screen",
    )

    # Define the RViz2 node
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        arguments=["-d", "/data/iw/config/rviz/iw_laser_matcher.rviz"],
    )

    return LaunchDescription(
        [
            # Declare all launch arguments
            DeclareLaunchArgument(
                "use_sim_time",
                default_value="false",
                description="Use simulation (Gazebo) clock if true",
            ),
            # Launch the laser_scan_matcher node
            laser_scan_matcher_node,
            # Launch RViz2
            rviz_node,
            # Call the service to enable laser odometry after a short delay
            TimerAction(period=2.0, actions=[enable_laser_odom]),
        ]
    )
