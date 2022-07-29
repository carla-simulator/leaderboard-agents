
#!/usr/bin/env python

# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

import nvtx

from srunner.scenariomanager.timer import GameTime

from leaderboard.autoagents.autonomous_agent import Track
from leaderboard.autoagents.npc_agent import NpcAgent


def get_entry_point():
    return 'ProfilerAgent'


class ProfilerAgent(NpcAgent):

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

    def __call__(self):
        with nvtx.annotate("AutonomousAgent.get_data", color="purple"):
            input_data = self.sensor_interface.get_data(GameTime.get_frame())

        timestamp = GameTime.get_time()

        if not self.wallclock_t0:
            self.wallclock_t0 = GameTime.get_wallclocktime()
        wallclock = GameTime.get_wallclocktime()
        wallclock_diff = (wallclock - self.wallclock_t0).total_seconds()

        print('======[Agent] Wallclock_time = {} / {} / Sim_time = {} / {}x'.format(wallclock, wallclock_diff, timestamp, timestamp/(wallclock_diff+0.001)))

        control = self.run_step(input_data, timestamp)
        control.manual_gear_shift = False

        return control

    @nvtx.annotate("AutonomousAgent.run_step", color="purple")
    def run_step(self, input_data, timestamp):
        return super(ProfilerAgent, self).run_step(input_data, timestamp)
