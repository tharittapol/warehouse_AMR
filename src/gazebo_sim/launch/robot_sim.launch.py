import os
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, ExecuteProcess, TimerAction, RegisterEventHandler
from launch.conditions import IfCondition
from launch.event_handlers import OnExecutionComplete
from launch.substitutions import LaunchConfiguration, Command, PathJoinSubstitution
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    # Constants for paths
    package_name_description = 'jetrover_description'
    default_robot_name = 'jetrover'
    package_name_gazebo = 'gazebo_sim'
    ros_gz_bridge_config_file_path = 'config/ros_gz_bridge.yaml'
    gazebo_worlds_path = 'worlds'
    world_file_name = 'industrial-warehouse.sdf'

    # Launch configuration variables
    use_gui = LaunchConfiguration('use_gui', default='false')
    use_rviz = LaunchConfiguration('use_rviz', default='false')
    namespace = LaunchConfiguration('namespace', default='')
    use_namespace = LaunchConfiguration('use_namespace', default='false')
    frame_prefix = LaunchConfiguration('frame_prefix', default='')
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    robot_name = LaunchConfiguration('robot_name', default=default_robot_name)
    world_file = LaunchConfiguration('world_file', default=world_file_name)

    x = LaunchConfiguration('x', default='0.0')
    y = LaunchConfiguration('y', default='0.0')
    z = LaunchConfiguration('z', default='0.1')
    roll = LaunchConfiguration('roll', default='0.0')
    pitch = LaunchConfiguration('pitch', default='0.0')
    yaw = LaunchConfiguration('yaw', default='0.0')

    # Paths
    description_pkg = FindPackageShare(
        package=package_name_description).find(package_name_description)
    ros_gz_sim_pkg = FindPackageShare(package='ros_gz_sim').find('ros_gz_sim')
    gazebo_sim_pkg = FindPackageShare(package=package_name_gazebo).find(package_name_gazebo)
    default_ros_gz_bridge_config_file_path = os.path.join(
        gazebo_sim_pkg, ros_gz_bridge_config_file_path)

    world_path = PathJoinSubstitution([
        gazebo_sim_pkg,
        gazebo_worlds_path,
        world_file
    ])

    # Include Robot State Publisher launch file
    robot_state_publisher_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(description_pkg, 'launch', 'robot_description.launch.py')
        ]),
        launch_arguments={
            'use_gui': use_gui,
            'use_rviz': use_rviz,
            'namespace': namespace,
            'use_namespace': use_namespace,
            'frame_prefix': frame_prefix,
            'use_sim_time': use_sim_time
        }.items()
    )

    # Start Gazebo
    start_gazebo_server_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim_pkg, 'launch', 'gz_sim.launch.py')),
        launch_arguments=[('gz_args', [' -r -s -v 4 ', world_path])])

    # Start Gazebo client (GUI)
    start_gazebo_client_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim_pkg, 'launch', 'gz_sim.launch.py')),
        launch_arguments={'gz_args': ['-g ']}.items()
    )

    # Bridge ROS topics and Gazebo messages for establishing communication
    start_gazebo_ros_bridge_cmd = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[{
            'config_file': default_ros_gz_bridge_config_file_path,
        }],
        output='screen')

    # Spawn the robot
    spawner_node = Node(
        package='ros_gz_sim',
        executable='create',
        output='screen',
        arguments=[
            '-topic', '/robot_description',
            '-name', robot_name,
            '-allow_renaming', 'true',
            '-x', x,
            '-y', y,
            '-z', z,
            '-R', roll,
            '-P', pitch,
            '-Y', yaw
        ]
    )


    # Create the launch description
    ld = LaunchDescription()

    # Add the actions to the launch description
    ld.add_action(robot_state_publisher_cmd)
    ld.add_action(start_gazebo_server_cmd)
    ld.add_action(start_gazebo_client_cmd)
    ld.add_action(start_gazebo_ros_bridge_cmd)
    ld.add_action(spawner_node)

    return ld
