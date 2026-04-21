import rclpy
from rclpy.node import Node

from nav_msgs.msg import Odometry
from std_msgs.msg import Float32
from nav2_msgs.action import NavigateToPose

import math
import time
import csv


class MonitorNode(Node):

    def __init__(self):
        super().__init__('monitor_node')

        # subscribe to odometry
        self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10
        )

        # subscribe to Nav2 goal
        self.create_subscription(
            NavigateToPose.Goal,
            '/navigate_to_pose/_action/goal',
            self.goal_callback,
            10
        )

        # publisher
        self.eff_pub = self.create_publisher(Float32, '/efficiency', 10)

        # variables
        self.prev_x = None
        self.prev_y = None

        self.start_x = None
        self.start_y = None

        self.goal_x = None
        self.goal_y = None

        self.path_length = 0.0
        self.start_time = None

        self.optimal_distance = 0.0
        self.battery = 100.0

        # CSV logging
        self.file = open('nav_metrics.csv', 'w', newline='')
        self.writer = csv.writer(self.file)
        self.writer.writerow(['time', 'path', 'distance', 'efficiency', 'battery'])

        print("Monitor node started")

    # ------------------------
    # ODOM CALLBACK
    # ------------------------
    def odom_callback(self, msg):

        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y

        print(f"x={x:.2f}, y={y:.2f}")

        # wait until goal received
        if self.goal_x is None or self.start_time is None:
            return

        # initialize start
        if self.start_x is None:
            self.start_x = x
            self.start_y = y

            dx = self.goal_x - x
            dy = self.goal_y - y
            self.optimal_distance = math.sqrt(dx**2 + dy**2)

        # compute path
        if self.prev_x is not None:
            dx = x - self.prev_x
            dy = y - self.prev_y
            step = math.sqrt(dx**2 + dy**2)

            self.path_length += step

            # battery model
            self.battery -= step * 0.5
            if self.battery < 0:
                self.battery = 0

        self.prev_x = x
        self.prev_y = y

        # distance to goal
        dx = self.goal_x - x
        dy = self.goal_y - y
        distance = math.sqrt(dx**2 + dy**2)

        # time
        elapsed = time.time() - self.start_time

        # efficiency
        efficiency = 0.0
        if self.path_length > 0:
            efficiency = self.optimal_distance / self.path_length

        # publish efficiency
        msg_eff = Float32()
        msg_eff.data = efficiency
        self.eff_pub.publish(msg_eff)

        # print
        print(
            f"time: {elapsed:.2f}s | "
            f"path: {self.path_length:.3f}m | "
            f"dist: {distance:.2f}m | "
            f"eff: {efficiency:.2f} | "
            f"battery: {self.battery:.1f}%"
        )

        # CSV logging
        self.writer.writerow([
            round(elapsed, 2),
            round(self.path_length, 3),
            round(distance, 2),
            round(efficiency, 2),
            round(self.battery, 1)
        ])
        self.file.flush()

    # ------------------------
    # GOAL CALLBACK
    # ------------------------
    def goal_callback(self, msg):

        self.goal_x = msg.pose.pose.position.x
        self.goal_y = msg.pose.pose.position.y

        # reset metrics
        self.start_time = time.time()
        self.path_length = 0.0
        self.prev_x = None
        self.prev_y = None
        self.start_x = None
        self.start_y = None
        self.optimal_distance = 0.0
        self.battery = 100.0

        print(f"New Nav2 Goal: ({self.goal_x:.2f}, {self.goal_y:.2f})")

    # ------------------------
    # CLEAN SHUTDOWN
    # ------------------------
    def destroy_node(self):
        self.file.close()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)

    node = MonitorNode()
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()