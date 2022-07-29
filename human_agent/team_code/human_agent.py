# Copyright (c) 2021 CVC.
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.


from leaderboard.autoagents.human_agent import HumanAgent as HumanAgent_


def get_entry_point():
    return "HumanAgent"


class HumanAgent(HumanAgent_):

    def sensors(self):
        sensors = [
            {'type': 'sensor.camera.rgb', 'x': 0.7, 'y': 0.0, 'z': 1.60, 'roll': 0.0, 'pitch': 0.0, 'yaw': 0.0,
             'width': 1280, 'height': 720, 'fov': 100, 'id': 'Center'},
        ]

        return sensors
