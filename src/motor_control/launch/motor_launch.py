from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    motor_node = Node(
        name="motor_sys",
        package='motor_control',
        executable='dc_motor',
        parameters=[{
            'sample_time': 0.01,
            'sys_gain_K': 2.16,
            'sys_tau_T': 0.05,
            'initial_conditions': 0.0,
        }]
    )
    
    # sp_node = Node(
    #     name="sp_gen",
    #     package='motor_control',
    #     executable='set_point',
    # )

    ctrl_node = Node(
        name="ctrl",
        package='motor_control',
        executable='controller',
        parameters=[{
            'kp': 0.5,
            'ki': 0.1,
            'kd': 0.01,
            'ts': 0.01,
        }]
    )
    
    return LaunchDescription([motor_node, ctrl_node])