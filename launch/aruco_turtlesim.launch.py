from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    camera_index = LaunchConfiguration('camera_index')
    show_window = LaunchConfiguration('show_window')

    return LaunchDescription([
        DeclareLaunchArgument(
            'camera_index',
            default_value='2',
            description='OpenCV camera index'
        ),
        DeclareLaunchArgument(
            'show_window',
            default_value='true',
            description='Show the OpenCV ArUco camera window'
        ),

        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='turtlesim',
            output='screen'
        ),

        Node(
            package='aruco_turtlesim_demo',
            executable='aruco_detector',
            name='aruco_detector',
            output='screen',
            parameters=[{
                'camera_index': camera_index,
                'show_window': show_window,
            }]
        ),

        Node(
            package='aruco_turtlesim_demo',
            executable='turtle_controller',
            name='turtle_controller',
            output='screen'
        ),
    ])
