# Copyright (c) 2021 CVC.
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

from leaderboard.autoagents.ros1_agent import ROS1Agent
from leaderboard.autoagents.autonomous_agent import Track


def get_entry_point():
    return "ROSMapAgent"


class ROSMapAgent(ROS1Agent):

    SENSOR_Z = 1.8

    def setup(self, path_to_conf_file):
        self.track = Track.MAP

    def sensors(self):
        sensors = [
            {
                'type': 'sensor.opendrive_map',
                'reading_frequency': 1,
                'id': 'ODM'
            },
            {
                'type': 'sensor.speedometer',
                'id': 'Speed'
            },
            {
                'type': 'sensor.other.gnss',
                'x': 0, 'y': 0, 'z': ROSMapAgent.SENSOR_Z,
                'id': 'GNSS'
            },
            {
                'type': 'sensor.other.imu',
                'x': 0, 'y': 0, 'z': 0,
                'roll': 0, 'pitch': 0, 'yaw': 0,
                'id': 'IMU'
            },
            {
                'type': 'sensor.lidar.ray_cast',
                'x': 0.7, 'y': 0.0, 'z': ROSMapAgent.SENSOR_Z,
                'roll': 0.0, 'pitch': 0.0, 'yaw': 0.0,
                'id': 'LIDAR'
            }
        ]

        return sensors

    def get_ros_entrypoint(self):
        return {
            "package": "ros_map_agent",
            "launch_file": "ros_map_agent.launch"
        }
