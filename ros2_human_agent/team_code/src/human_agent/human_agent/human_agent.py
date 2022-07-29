# Copyright (c) 2022 CVC.
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

import copy
import threading

import rclpy
import rclpy.node
import rclpy.qos

import carla
import numpy
from leaderboard.autoagents.human_agent import HumanInterface, KeyboardControl

from carla_msgs.msg import CarlaEgoVehicleControl, CarlaSpeedometer, CarlaRoute, CarlaGnssRoute
from sensor_msgs.msg import Image
from std_msgs.msg import Bool


class HumanAgent(rclpy.node.Node):

    FREQUENCY = 20  # Hz

    def __init__(self):
        super().__init__('human_agent', parameter_overrides=[rclpy.Parameter("use_sim_time", rclpy.Parameter.Type.BOOL, True)])

        self._hic = HumanInterface(800, 600, 1)
        self._controller = KeyboardControl(path_to_conf_file=None)
        self.data_lock = threading.Lock()
        self._input_data = None

        self._camera_subscriber = self.create_subscription(Image, "/carla/hero/Center/image", self._on_camera, 10)
        self._speedometer_subscriber = self.create_subscription(CarlaSpeedometer, "/carla/hero/Speed", self._on_speedometer, 10)
        self._path_subscriber = self.create_subscription(CarlaRoute, "/carla/hero/global_plan", self._on_path, rclpy.qos.DurabilityPolicy.TRANSIENT_LOCAL)
        self._path_gnss_subscriber = self.create_subscription(CarlaGnssRoute, "/carla/hero/global_plan_gnss", self._on_path_gnss, rclpy.qos.DurabilityPolicy.TRANSIENT_LOCAL)
        self._vehicle_control_cmd_publisher = self.create_publisher(CarlaEgoVehicleControl, "/carla/hero/vehicle_control_cmd", 1)

        self.create_timer(1.0 / HumanAgent.FREQUENCY, self.run_step)

        ready = self.create_publisher(Bool, "/carla/hero/status", qos_profile=rclpy.qos.QoSProfile(depth=1, durability=rclpy.qos.DurabilityPolicy.TRANSIENT_LOCAL))
        ready.publish(Bool(data=True))

    def _on_camera(self, image):
        array = numpy.frombuffer(image.data, dtype=numpy.dtype("uint8"))
        array = numpy.reshape(array, (image.height, image.width, 4))
        with self.data_lock:
            self._input_data = {'Center': (0, array)}

    def _on_speedometer(self, speed):
        pass
        #self.get_logger().info(str(speed.speed))

    def _on_path(self, global_plan):
        self.get_logger().info(str(global_plan.road_options))

    def _on_path_gnss(self, global_plan_gnss):
        self.get_logger().info(str(global_plan_gnss.road_options))

    def run_step(self):
        with self.data_lock:
            input_data = copy.deepcopy(self._input_data)

        if input_data is not None:
            self._hic.run_interface(self._input_data)
            control = self._controller.parse_events(1.0/HumanAgent.FREQUENCY)
        else:
            control = carla.VehicleControl()

        control_msg = CarlaEgoVehicleControl()
        control_msg.header.stamp = self.get_clock().now().to_msg()
        control_msg.steer = control.steer
        control_msg.throttle = control.throttle
        control_msg.brake = control.brake
        control_msg.hand_brake = control.hand_brake
        control_msg.reverse = control.reverse
        control_msg.manual_gear_shift = control.manual_gear_shift
        control_msg.gear = control.gear

        self._vehicle_control_cmd_publisher.publish(control_msg)


def main(args=None):
    rclpy.init(args=args)
    human_agent = HumanAgent()
    rclpy.spin(human_agent)
    human_agent.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
