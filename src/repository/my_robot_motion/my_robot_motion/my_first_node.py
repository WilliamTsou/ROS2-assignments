import math
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState


class TrajectoryPublisher(Node):
    def __init__(self):
        super().__init__('trajectory_publisher')

        self.joint_names = [
            'arm_0_joint',
            'arm_1_joint',
            'arm_2_joint',
            'gripper_1_joint',
            'gripper_2_joint',
        ]

        self.waypoints = [
            [0.0,  0.0,  0.0,  0.00, 0.00],
            [1.0,  0.5, -0.5,  0.03, 0.03],
            [-1.0, -0.5,  0.5,  0.05, 0.05],
            [0.5,  1.0, -1.0,  0.00, 0.00],
            [-0.5, -1.0,  1.0,  0.02, 0.02],
        ]

        self.segment_duration = 3.0
        self.elapsed_in_segment = 0.0
        self.current_index = 0

        self.publisher_ = self.create_publisher(JointState, '/joint_states', 10)

        self.timer = self.create_timer(0.05, self.timer_callback)

    def ease(self, t):
        return 0.5 * (1.0 - math.cos(math.pi * t))

    def timer_callback(self):
        t = self.elapsed_in_segment / self.segment_duration
        alpha = self.ease(min(t, 1.0))

        start = self.waypoints[self.current_index]
        end_index = (self.current_index + 1) % len(self.waypoints)
        end = self.waypoints[end_index]

        positions = [
            start[i] + (end[i] - start[i]) * alpha
            for i in range(len(self.joint_names))
        ]

        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = self.joint_names
        msg.position = positions
        self.publisher_.publish(msg)

        self.elapsed_in_segment += 0.05
        if self.elapsed_in_segment >= self.segment_duration:
            self.elapsed_in_segment = 0.0
            self.current_index = end_index


def main(args=None):
    rclpy.init(args=args)
    node = TrajectoryPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
