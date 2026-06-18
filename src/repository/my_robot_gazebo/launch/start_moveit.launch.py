from launch import LaunchDescription
from launch_ros.actions import Node, SetParameter
from moveit_configs_utils import MoveItConfigsBuilder


def generate_launch_description():
    moveit_config = MoveItConfigsBuilder(
        "my_arm", package_name="arm_moveit_config"
    ).to_dict()

    return LaunchDescription([
        SetParameter(name='use_sim_time', value=True),
        Node(
            package="moveit_ros_move_group",
            executable="move_group",
            output="screen",
            parameters=[moveit_config],
        ),
    ])
