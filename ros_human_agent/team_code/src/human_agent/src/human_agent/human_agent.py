# Copyright (c) 2021 CVC.
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

import copy
import threading

import rospy

import carla
import numpy
from leaderboard.autoagents.human_agent import HumanInterface, KeyboardControl

from carla_msgs.msg import CarlaEgoVehicleControl
from sensor_msgs.msg import Image
from std_msgs.msg import Bool


class HumanAgent(object):

    FREQUENCY = 20  # Hz

    def __init__(self):
        self._hic = HumanInterface()
        self._controller = KeyboardControl(path_to_conf_file=None)
        self.data_lock = threading.Lock()
        self._input_data = None

        self._camera_subscriber = rospy.Subscriber("/carla/hero/Center/image", Image, self._on_camera, queue_size=10)
        self._vehicle_control_cmd_publisher = rospy.Publisher("/carla/hero/vehicle_control_cmd", CarlaEgoVehicleControl, queue_size=1)

        rospy.Timer(rospy.Duration(1.0 / HumanAgent.FREQUENCY), self.run_step)

        ready = rospy.Publisher("/carla/hero/status", Bool, latch=True, queue_size=1)
        ready.publish(True)

    def _on_camera(self, image):
        array = numpy.frombuffer(image.data, dtype=numpy.dtype("uint8"))
        array = numpy.reshape(array, (image.height, image.width, 4))
        with self.data_lock:
            self._input_data = {'Center': (image.header.seq, array)}

    def run_step(self, event):
        with self.data_lock:
            input_data = copy.deepcopy(self._input_data)

        if input_data is not None:
            self._hic.run_interface(self._input_data)
            control = self._controller.parse_events(event.current_expected.to_sec() - event.last_expected.to_sec())
        else:
            control = carla.VehicleControl()

        control_msg = CarlaEgoVehicleControl()
        control_msg.header.stamp = rospy.Time.now()
        control_msg.steer = control.steer
        control_msg.throttle = control.throttle
        control_msg.brake = control.brake
        control_msg.hand_brake = control.hand_brake
        control_msg.reverse = control.reverse
        control_msg.manual_gear_shift = control.manual_gear_shift
        control_msg.gear = control.gear

        self._vehicle_control_cmd_publisher.publish(control_msg)
