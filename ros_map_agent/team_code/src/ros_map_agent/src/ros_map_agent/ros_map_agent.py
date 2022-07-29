# Copyright (c) 2021 CVC.
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

import math
import queue
import time
import threading

import rospy
import message_filters
import tf2_ros

import carla
import numpy as np
import transforms3d

from map_agent.map_agent import MapAgent

import carla_common.transforms as trans
from agents.navigation.local_planner import RoadOption

from carla_msgs.msg import CarlaEgoVehicleControl, CarlaSpeedometer, CarlaRoute
from sensor_msgs.msg import Imu
from sensor_msgs.msg import NavSatFix
from sensor_msgs.msg import PointCloud2
from std_msgs.msg import Bool
from std_msgs.msg import Float32
from std_msgs.msg import String
from visualization_msgs.msg import Marker


def _parse_pointcloud2(lidar_msg):
    array = np.fromstring(bytes(lidar_msg.data), dtype=np.float32)
    array = np.reshape(array, (int(array.shape[0] / 4), 4))
    array[:, 1] *= -1
    return array


def _parse_gnss(gnss_msg):
    array = np.array([
        gnss_msg.latitude,
        gnss_msg.longitude,
        gnss_msg.altitude
    ], dtype=np.float64)
    return array


def _parse_imu(imu_msg):
    roll, pitch, _ = transforms3d.euler.quat2euler([
        imu_msg.orientation.w,
        imu_msg.orientation.x,
        imu_msg.orientation.y,
        imu_msg.orientation.z])
    array = np.array([
        imu_msg.linear_acceleration.x,
       -imu_msg.linear_acceleration.y ,
        imu_msg.linear_acceleration.z,
       -imu_msg.angular_velocity.x,
        imu_msg.angular_velocity.y,
       -imu_msg.angular_velocity.z,
       -math.atan2(roll, pitch) + 2*math.pi,
    ], dtype=np.float64)
    return array


class ROSMapAgent(object):

    FREQUENCY = 20  # Hz

    def __init__(self):
        self._agent = None

        self._data_lock = threading.Lock()
        self._odr_map = None
        self._speed = 0
        self._sensors_data = {}
        self._sensors_timestamp = 0
        self._sensors_queue = queue.Queue(1)

        #self._plan_subscriber = rospy.Subscriber("/carla/hero/global_plan", CarlaRoute, self._plan_cb)
        #self._map_subscriber = rospy.Subscriber("/carla/hero/ODM", String, self._map_cb)

        self._speedometer_subscriber = message_filters.Subscriber("/carla/hero/Speed", CarlaSpeedometer)
        self._gnss_subscriber = message_filters.Subscriber("/carla/hero/GNSS", NavSatFix)
        self._imu_subscriber = message_filters.Subscriber("/carla/hero/IMU", Imu)
        self._lidar_subscriber = message_filters.Subscriber("/carla/hero/LIDAR", PointCloud2)

        ts = message_filters.TimeSynchronizer([
            self._speedometer_subscriber,
            self._gnss_subscriber,
            self._imu_subscriber,
            self._lidar_subscriber
        ], 10)
        ts.registerCallback(self._sensors_cb)

        self._tf_broadcaster = tf2_ros.TransformBroadcaster()

        self._vehicle_control_cmd_publisher = rospy.Publisher("/carla/hero/vehicle_control_cmd", CarlaEgoVehicleControl, queue_size=1)
        self._current_pose_marker_publisher = rospy.Publisher("/current_pose", Marker, queue_size=1)
        self._target_pose_marker_publisher = rospy.Publisher("/target_pose", Marker, queue_size=1)

        rospy.Timer(rospy.Duration(1.0 / ROSMapAgent.FREQUENCY), self.run_step)

        ready = rospy.Publisher("/carla/hero/status", Bool, latch=True, queue_size=1)
        ready.publish(True)

        #status = rospy.wait_for_message("/carla/leadeboard/status", Bool)
        #rospy.Timer(rospy.Duration(1.0 / ADMapAgent.FREQUENCY), self.run_step)

        # map_data =  rospy.wait_for_message("/carla/hero/ODM", String, 10)

        plan_data = rospy.wait_for_message("/carla/hero/global_plan", CarlaRoute, 30)
        self._agent = MapAgent([
            (trans.ros_pose_to_carla_transform(pose), RoadOption(int(road_option))) for pose, road_option in zip(plan_data.poses, plan_data.road_options)
        ])
        rospy.loginfo("Agent initialized")

        map_data =  rospy.wait_for_message("/carla/hero/ODM", String, 30)
        self._odr_map = map_data.data
        rospy.loginfo("Map received")

    def _plan_cb(self, data):
        if self._agent is None:
            global_plan = [
                (trans.ros_pose_to_carla_transform(pose), RoadOption(int(road_option))) for pose, road_option in zip(data.poses, data.road_options)
            ]
            with self._data_lock:
                self._agent = MapAgent(global_plan)
                rospy.loginfo("MapAgent initialized")

    def _map_cb(self, data):
        rospy.loginfo("Map received")
        with self._data_lock:
            self._odr_map = data.data

    def _sensors_cb(self, speed_data, gnss_data, imu_data, lidar_data):
        assert speed_data.header.stamp == gnss_data.header.stamp == imu_data.header.stamp == lidar_data.header.stamp

        sensors_timestamp = gnss_data.header.stamp
        sensors_data = {
           "Speed": (speed_data.header.seq, {"speed": speed_data.speed}),
           "GNSS": (gnss_data.header.seq, _parse_gnss(gnss_data)),
           "IMU": (imu_data.header.seq, _parse_imu(imu_data)),
           "LIDAR": (lidar_data.header.seq, _parse_pointcloud2(lidar_data)),
        }
        try:
            self._sensors_queue.put_nowait((sensors_timestamp, sensors_data))
        except queue.Full:
            rospy.logwarn("Sensors not processed")

    def run_step(self, event):

        #with self._data_lock:
        #    if self._agent is not None and self._agen
        # odr_map = None
        # if self._agent is not None and not self._agent._map_initialized:
        #     with self._data_lock:
        #         if self._odr_map is not None:
        #             pass

        sensors_timestamp, sensors_data = None, None
        try:
            sensors_timestamp, sensors_data = self._sensors_queue.get(True, 1)
        except queue.Empty:
            rospy.logwarn("We haven't received sensor data")

        control, status, target = carla.VehicleControl(), None, None

        print(sensors_timestamp)
        if sensors_data is not None:
            if not self._agent._map_initialized:
                rospy.loginfo("Initializing agent with map data...")
                sensors_data["ODM"] = (0, {"opendrive": self._odr_map})


            rospy.loginfo("1")
            #control, status, target = self._agent.run_step(sensors_data, sensors_timestamp.to_sec())
            control, status, target = carla.VehicleControl(), None, None
            time.sleep(0.1)
            rospy.loginfo("map_agent run step done")

            # with self._data_lock:
            #     running = self._agent is not None
            #     if self._odr_map is not None:
            #         rospy.loginfo("Initializing agent with map data...")
            #         sensors_data["ODM"] = (0, {"opendrive": self._odr_map})
            #         #self._odr_map = None

            # if running:
            #     rospy.loginfo("1")
            #     control, status, target = self._agent.run_step(sensors_data, sensors_timestamp.to_sec())
            #     rospy.loginfo("map_agent run step done")


        if status:
            marker_msg = Marker()
            marker_msg.header.frame_id = "map"
            marker_msg.header.stamp = event.current_real
            marker_msg.id = 0
            marker_msg.type = Marker.CUBE
            marker_msg.color.r = 0.0
            marker_msg.color.g = 255.0
            marker_msg.color.b = 0.0
            marker_msg.color.a = 0.3

            marker_msg.pose = trans.carla_transform_to_ros_pose(status[0])
            marker_msg.scale.x = 2.0
            marker_msg.scale.y = 1.0
            marker_msg.scale.z = 1.0

            self._current_pose_marker_publisher.publish(marker_msg)

            # Publish tf
            transform = tf2_ros.TransformStamped()
            transform.header.stamp = event.current_real
            transform.header.frame_id = "map"
            transform.child_frame_id = "hero"
            transform.transform = trans.carla_transform_to_ros_transform(status[0])

            self._tf_broadcaster.sendTransform(transform)

        if target:
            marker_msg = Marker()
            marker_msg.header.frame_id = "map"
            marker_msg.header.stamp = event.current_real
            marker_msg.id = 0
            marker_msg.type = Marker.SPHERE
            marker_msg.color.r = 0.0
            marker_msg.color.r = 255.0
            marker_msg.color.r = 0.0
            marker_msg.color.a = 0.3

            marker_msg.pose = trans.carla_location_to_pose(target[0])
            marker_msg.scale.x = 1.0
            marker_msg.scale.y = 1.0
            marker_msg.scale.z = 1.0

            self._target_pose_marker_publisher.publish(marker_msg)

        control_msg = CarlaEgoVehicleControl()
        control_msg.header.stamp = event.current_expected if sensors_timestamp is None else sensors_timestamp
        control_msg.steer = control.steer
        control_msg.throttle = control.throttle
        control_msg.brake = control.brake
        control_msg.hand_brake = control.hand_brake
        control_msg.reverse = control.reverse
        control_msg.manual_gear_shift = control.manual_gear_shift
        control_msg.gear = control.gear

        rospy.loginfo("Publishing vehicle control")
        self._vehicle_control_cmd_publisher.publish(control_msg)
 