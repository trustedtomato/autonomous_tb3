#!/usr/bin/env python3

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    pkg_path = get_package_share_directory('autonomous_tb3')
    launch_file_dir = os.path.join(get_package_share_directory('turtlebot3_gazebo'), 'launch')
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    world_path = os.path.join(pkg_path, 'world', 'model.sdf')
    map_path = os.path.join(pkg_path, 'config', 'map.yaml')
    nav_params_path = os.path.join(pkg_path, 'config', 'tb3_nav_params.yaml')
    nav_rviz_config = os.path.join(pkg_path, 'config', 'tb3_nav.rviz')

    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    # original position of the robot - modified according to the exam requirements
    x_pose = LaunchConfiguration('x_pose', default='1.7')
    y_pose = LaunchConfiguration('y_pose', default='-1.5')

    return LaunchDescription([

        # these are all from https://github.com/ROBOTIS-GIT/turtlebot3_simulations/blob/humble-devel/turtlebot3_gazebo/launch/turtlebot3_world.launch.py
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg_gazebo_ros, 'launch', 'gzserver.launch.py')
            ),
            # launch_arguments={'world': world}.items()
        ),

        # IncludeLaunchDescription(
        #     PythonLaunchDescriptionSource(
        #         os.path.join(pkg_gazebo_ros, 'launch', 'gzclient.launch.py')
        #     )
        # ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(launch_file_dir, 'robot_state_publisher.launch.py')
            ),
            launch_arguments=({'use_sim_time': use_sim_time}.items())
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(launch_file_dir, 'spawn_turtlebot3.launch.py')
            ),
            launch_arguments=({
                'x_pose': x_pose,
                'y_pose': y_pose
            }.items())
        ),

        # add our own SDF
        Node(
            package='autonomous_tb3',
            output='screen',
            executable='sdf_spawner',
            name='sdf_spawner',
            arguments=[world_path, 'b', '1.0', '1.0']
        ),

        # navigation
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                os.path.join(
                    get_package_share_directory('nav2_bringup'),
                    'launch',
                    'bringup_launch.py'
                )
            ]),
            launch_arguments={
                'map': map_path,
                'params_file': nav_params_path
            }.items()
        ),

        Node(
            package='rviz2',
            executable='rviz2',
            output={'both': 'log'},
            name='rviz2_node',
            arguments=['-d', nav_rviz_config]
        ),

        # commanding
        # Node(
        #     package='autonomous_tb3',
        #     output='screen',
        #     executable='commander',
        #     name='commander'
        # ),
    ])