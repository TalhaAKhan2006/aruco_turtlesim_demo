#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
from geometry_msgs.msg import Twist


class TurtleControllerNode(Node):
    """
    Convert six ArUco IDs into timed turtlesim commands.

    ID 1: Turn left
    ID 2: Move up/forward
    ID 3: Turn right
    ID 4: Move down/backward
    ID 5: Move forward
    ID 6: Move backward

    Note: turtlesim is a 2D simulator. "Up" and "down" here mean
    screen/world movement after the turtle has been oriented appropriately.
    """

    def __init__(self):
        super().__init__('turtle_controller')

        self.declare_parameter('linear_speed', 1.0)
        self.declare_parameter('angular_speed', 1.5)
        self.declare_parameter('move_duration', 0.75)
        self.declare_parameter('turn_duration', 0.75)

        self.linear_speed = float(self.get_parameter('linear_speed').value)
        self.angular_speed = float(self.get_parameter('angular_speed').value)
        self.move_duration = float(self.get_parameter('move_duration').value)
        self.turn_duration = float(self.get_parameter('turn_duration').value)

        self.cmd_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.marker_sub = self.create_subscription(
            Int32,
            '/aruco_marker_id',
            self.marker_callback,
            10
        )

        self.stop_timer = None

        self.get_logger().info('Turtle controller started.')
        self.get_logger().info(
            '1=left, 2=up/forward, 3=right, 4=down/backward, '
            '5=forward, 6=backward'
        )

    def marker_callback(self, msg):
        marker_id = int(msg.data)

        if marker_id == 1:
            self.execute_turn(+1.0, self.turn_duration, 'LEFT')

        elif marker_id == 2:
            self.execute_move(+1.0, self.move_duration, 'UP / FORWARD')

        elif marker_id == 3:
            self.execute_turn(-1.0, self.turn_duration, 'RIGHT')

        elif marker_id == 4:
            self.execute_move(-1.0, self.move_duration, 'DOWN / BACKWARD')

        elif marker_id == 5:
            self.execute_move(+1.0, self.move_duration, 'FORWARD')

        elif marker_id == 6:
            self.execute_move(-1.0, self.move_duration, 'BACKWARD')

        else:
            self.get_logger().warn(f'Ignoring unknown marker ID: {marker_id}')

    def execute_move(self, direction, duration, name):
        self.cancel_stop_timer()

        twist = Twist()
        twist.linear.x = direction * self.linear_speed
        self.cmd_pub.publish(twist)

        self.get_logger().info(
            f'[ACTION] Marker command: {name} for {duration:.2f} s'
        )

        self.stop_timer = self.create_timer(
            duration,
            self.stop_motion,
            callback_group=None
        )

    def execute_turn(self, direction, duration, name):
        self.cancel_stop_timer()

        twist = Twist()
        twist.angular.z = direction * self.angular_speed
        self.cmd_pub.publish(twist)

        self.get_logger().info(
            f'[ACTION] Marker command: TURN {name} for {duration:.2f} s'
        )

        self.stop_timer = self.create_timer(
            duration,
            self.stop_motion,
            callback_group=None
        )

    def stop_motion(self):
        twist = Twist()
        self.cmd_pub.publish(twist)

        if self.stop_timer is not None:
            self.stop_timer.cancel()
            self.stop_timer = None

        self.get_logger().info('[ACTION] STOP')

    def cancel_stop_timer(self):
        if self.stop_timer is not None:
            self.stop_timer.cancel()
            self.stop_timer = None


def main(args=None):
    rclpy.init(args=args)
    node = TurtleControllerNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.stop_motion()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
