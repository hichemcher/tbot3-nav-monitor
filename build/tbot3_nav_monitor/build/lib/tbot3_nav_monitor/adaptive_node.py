import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from std_msgs.msg import Float32


class AdaptiveNode(Node):

    def __init__(self):
        super().__init__('adaptive_node')

        # receive velocity
        self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_callback,
            10
        )

        # receive efficiency
        self.create_subscription(
            Float32,
            '/efficiency',
            self.eff_callback,
            10
        )

        # publish new velocity
        self.pub = self.create_publisher(
            Twist,
            '/cmd_vel_adapted',
            10
        )

        self.slow_mode = False

        print("Adaptive node started")

    # ------------------------
    # efficiency callback
    # ------------------------
    def eff_callback(self, msg):
        if msg.data < 0.6:
            self.slow_mode = True
        else:
            self.slow_mode = False

    # ------------------------
    # velocity callback
    # ------------------------
    def cmd_callback(self, msg):

        new_msg = Twist()

        # copy original
        new_msg.linear.x = msg.linear.x
        new_msg.angular.z = msg.angular.z

        # apply adaptation
        if self.slow_mode:
            new_msg.linear.x *= 0.5
            new_msg.angular.z *= 0.5

        self.pub.publish(new_msg)


def main():
    rclpy.init()
    node = AdaptiveNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
