from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    # 1. The Motor Node (Existing)
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
    
    # 2. The Set Point Generator (Existing)
    sp_node = Node(
        name="sp_gen",
        package='motor_control',
        executable='set_point',
    )

    # 3. The Controller Node (NEW)
    # This node closes the loop by connecting sp_gen and motor_sys [cite: 46, 125]
    ctrl_node = Node(
        name="ctrl",
        package='motor_control',
        executable='controller', # The name you'll define in setup.py
        parameters=[{
            'kp': 0.5,
            'ki': 0.1,
            'kd': 0.01,
            'ts': 0.01,
        }]
    )
    
    return LaunchDescription([motor_node, sp_node, ctrl_node])