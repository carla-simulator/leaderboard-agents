
#!/usr/bin/env python

# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

from leaderboard.autoagents.autonomous_agent import Track
from leaderboard.autoagents.npc_agent import NpcAgent


def get_entry_point():
    return 'BenchmarkAgent'


class BenchmarkAgent(NpcAgent):

    def setup(self, path_to_conf_file):
        self.track = Track.SENSORS

    def sensors(self):
        sensors = [
            {'type': 'sensor.camera.rgb', 'x': 0.7, 'y': -0.4, 'z': 1.60, 'roll': 0.0, 'pitch': 0.0, 'yaw': 0.0,
             'width': 1920, 'height': 1080, 'fov': 100, 'id': 'Camera1'},
            {'type': 'sensor.camera.rgb', 'x': 0.7, 'y': -0.4, 'z': 1.60, 'roll': 0.0, 'pitch': 0.0, 'yaw': 0.0,
             'width': 1920, 'height': 1080, 'fov': 100, 'id': 'Camera2'},
        ]

        return sensors

    def run_step(self, input_data, timestamp):
        return super(NpcAgent, self).run_step(input_data, timestamp)
