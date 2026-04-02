import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, GroupAction, LogInfo
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import PushRosNamespace, SetRemap
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
import subprocess

tiago_custom_nav2_pkg_share = get_package_share_directory('tiago_custom_nav2')


def generate_launch_description():

    param_file = os.path.join(tiago_custom_nav2_pkg_share, 'config', 'tiago_custom_nav2.yaml')
    return LaunchDescription([
       GroupAction([

            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(
                        get_package_share_directory('nav2_bringup'),
                        'launch',
                        'navigation_launch.py'
                    )
                ),
                launch_arguments={
                    "params_file": param_file,
                    "use_sim_time": "false",
                }.items()
            ),
        ]),
    ])