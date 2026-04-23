from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    default_waypoints_file = PathJoinSubstitution(
        [FindPackageShare('tiago_movement_behaviours'), 'configs', 'patrol_south6th.yaml']
    )

    waypoints_file_arg = DeclareLaunchArgument(
        'waypoints_file',
        default_value=default_waypoints_file,
        description='Absolute path to YAML file containing patrol waypoints',
    )

    patrol_node = Node(
        package='tiago_movement_behaviours',
        executable='tiago_custom_patrol',
        name='nav_action_client',
        output='screen',
        parameters=[
            {
                'waypoints_file': LaunchConfiguration('waypoints_file'),
            }
        ],
    )

    return LaunchDescription([
        waypoints_file_arg,
        patrol_node,
    ])
