# Copyright (c) 2021 CVC.
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

from leaderboard.autoagents.autonomous_agent import Track
from leaderboard.autoagents.human_agent import HumanAgent as HumanAgent_
from leaderboard.autoagents.human_agent import KeyboardControl as KeyboardControl_
from leaderboard.autoagents.human_agent import HumanInterface
from srunner.scenariomanager.carla_data_provider import CarlaDataProvider


def get_entry_point():
    return "HumanAgent"


class HumanAgent(HumanAgent_):

    def setup(self, path_to_conf_file):

        self.track = Track.SENSORS

        # Get the ego instance
        self._player = None

        for vehicle in CarlaDataProvider.get_world().get_actors().filter('vehicle.*'):
            if vehicle.attributes['role_name'] == 'hero':
                self._player = vehicle
                break

        if self._player is None:
            raise ValueError("Couldn't find the ego vehicle")

        self.agent_engaged = False
        self.camera_width = 1280
        self.camera_height = 720
        self._side_scale = 0.3
        self._left_mirror = False
        self._right_mirror = False

        self._hic = HumanInterface(
            self.camera_width,
            self.camera_height,
            self._side_scale,
            self._left_mirror,
            self._right_mirror
        )
        self._controller = KeyboardControl(self._player, path_to_conf_file)
        self._prev_timestamp = 0


class KeyboardControl(KeyboardControl_):

    def __init__(self, player, path_to_conf_file):
        self._player = player
        super().__init__(path_to_conf_file)

    def _record_control(self):

        velocity = self._player.get_velocity()
        acceleration = self._player.get_acceleration()
        transform = self._player.get_transform()

        new_record = {
            'control': {
                'throttle': round(self._control.throttle, 2),
                'steer': round(self._control.steer, 2),
                'brake': round(self._control.brake, 2),
                'hand_brake': self._control.hand_brake,
                'reverse': self._control.reverse,
                'manual_gear_shift': self._control.manual_gear_shift,
                'gear': self._control.gear
            },
            'state': {
                'velocity': {
                    'x': round(velocity.x, 1),
                    'y': round(velocity.y, 1),
                    'z': round(velocity.z, 1),
                    'value': round(velocity.length(), 1)
                },
                'acceleration': {
                    'x': round(acceleration.x, 1),
                    'y': round(acceleration.y, 1),
                    'z': round(acceleration.z, 1),
                    'value': round(acceleration.length(), 1)
                },
                'transform': {
                    'x': round(transform.location.x, 1),
                    'y': round(transform.location.y, 1),
                    'z': round(transform.location.z, 1),
                    'roll': round(transform.rotation.roll, 1),
                    'pitch': round(transform.rotation.pitch, 1),
                    'yaw': round(transform.rotation.yaw, 1)
                }
            }
        }

        self._log_data['records'].append(new_record)
