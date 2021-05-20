# Copyright (c) 2021 CVC.
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

from leaderboard.autoagents.ros1_agent import ROS1Agent
from leaderboard.autoagents.autonomous_agent import Track


def get_entry_point():
    return "ROSHumanAgent"


class ROSHumanAgent(ROS1Agent):

    def setup(self, path_to_conf_file):
        self.track = Track.SENSORS

    def sensors(self):
        sensors = [
            {'type': 'sensor.camera.rgb', 'x': 0.7, 'y': 0.0, 'z': 1.60, 'roll': 0.0, 'pitch': 0.0, 'yaw': 0.0,
             'width': 800, 'height': 600, 'fov': 100, 'id': 'Center'},
        ]

        return sensors

    def get_ros_entrypoint(self):
        return {
            "package": "human_agent",
            "launch_file": "human_agent.launch"
        }
