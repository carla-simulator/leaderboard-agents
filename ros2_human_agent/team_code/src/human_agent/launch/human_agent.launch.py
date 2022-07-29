import os

import launch
import launch_ros.actions

from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    ld = launch.LaunchDescription([
        launch_ros.actions.Node(
            package='human_agent',
            executable='human_agent',
            name=['human_agent'],
            output='screen',
        ),
        launch_ros.actions.Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=[
                '-d', os.path.join(get_package_share_directory('human_agent'), 'config.rviz')],
            on_exit=launch.actions.Shutdown()
        )
    ])
    return ld


if __name__ == '__main__':
    generate_launch_description()