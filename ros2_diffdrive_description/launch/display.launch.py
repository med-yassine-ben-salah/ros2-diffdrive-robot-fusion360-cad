import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    pkg_share = get_package_share_directory("ros2_diffdrive_description")
    xacro_file = os.path.join(pkg_share, "urdf", "ros2_diffdrive_robot.urdf.xacro")
    rviz_file = os.path.join(pkg_share, "rviz", "display.rviz")

    use_gui = LaunchConfiguration("use_gui")
    use_ros2_control = LaunchConfiguration("use_ros2_control")
    use_sim = LaunchConfiguration("use_sim")
    publish_odom_tf = LaunchConfiguration("publish_odom_tf")

    robot_description_content = ParameterValue(
        Command([
            PathJoinSubstitution([FindExecutable(name="xacro")]),
            " ", xacro_file,
            " use_ros2_control:=", use_ros2_control,
            " use_sim:=", use_sim,
            " publish_odom_tf:=", publish_odom_tf,
        ]),
        value_type=str,
    )

    return LaunchDescription([
        DeclareLaunchArgument("use_gui", default_value="true",
                              description="Start joint_state_publisher_gui"),
        DeclareLaunchArgument("use_ros2_control", default_value="true",
                              description="Enable ros2_control hardware plugin"),
        DeclareLaunchArgument("use_sim", default_value="false",
                              description="Use GazeboSystem when true, MyBotSystem when false"),
        DeclareLaunchArgument("publish_odom_tf", default_value="true",
                              description="Publish odom -> base_footprint TF in legacy diff_drive plugin"),
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            name="robot_state_publisher",
            output="both",
            parameters=[{"robot_description": robot_description_content}],
        ),
        Node(
            package="joint_state_publisher_gui",
            executable="joint_state_publisher_gui",
            name="joint_state_publisher_gui",
            condition=IfCondition(use_gui),
        ),
        Node(
            package="rviz2",
            executable="rviz2",
            name="rviz2",
            output="screen",
            arguments=["-d", rviz_file],
            parameters=[{
                "transforms.default_cache_time": 30.0,
                "transforms.max_cache_time": 60.0,
            }],
        ),
    ])
