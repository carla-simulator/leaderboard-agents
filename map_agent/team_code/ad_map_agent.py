# Copyright (c) # Copyright (c) 2018-2021 CVC.
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

"""
This module provides an example of an agent that doesn't use the carla.Map in order to
navigate through the town, by using the (https://github.com/carla-simulator/map) library,
which doesn't access any privileged information.
"""

from __future__ import print_function

from leaderboard.autoagents.autonomous_agent import AutonomousAgent, Track
from map_agent.map_agent import MapAgent


def get_entry_point():
    return 'ADMapAgent'


class ADMapAgent(AutonomousAgent):
    """
    Autonomous agent to control the ego vehicle using the AD Map library
    to parse the opendrive map information
    """

    def setup(self, path_to_conf_file):
        """Setup the agent parameters"""
        self.track = Track.MAP
        self._map_agent = MapAgent(self._global_plan_world_coord)

    def sensors(self):
        """Define the sensors required by the agent. IMU and GNSS are setup at the
        same position to avoid having to change between those two coordinate references"""
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
                'x': 0, 'y': 0, 'z': self._map_agent._sensor_z,
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
                'x': 0.7, 'y': 0.0, 'z': self._map_agent._sensor_z,
                'roll': 0.0, 'pitch': 0.0, 'yaw': 0.0,
                'id': 'LIDAR'
            }
        ]

        return sensors

    def run_step(self, data, timestamp):
        """Execute one step of navigation."""
        control, _, _ = self._map_agent.run_step(data, timestamp)
        return control

    def destroy(self):
        """Remove the AD map library files"""
        self._map_agent.destroy()
        super().destroy()
