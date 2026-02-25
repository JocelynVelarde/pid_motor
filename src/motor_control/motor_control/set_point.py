import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
import numpy as np
import time
import threading
from custom_interfaces.srv import SetProcessBool


class SetPointGenerator(Node):
    def __init__(self):
        super().__init__('sp_gen')
        self.publisher_ = self.create_publisher(Float32, '/set_point', 10)

        # Add this inside your SetPointGenerator.__init__ function:
        self.cli_motor = self.create_client(
            SetProcessBool, '/motor_sys/set_enable')
        self.cli_ctrl = self.create_client(SetProcessBool, '/ctrl/set_enable')

        # Start a background thread for keyboard input
        self.keyboard_thread = threading.Thread(target=self.keyboard_listener)
        self.keyboard_thread.daemon = True
        self.keyboard_thread.start()

    # Add these new methods to the SetPointGenerator class:
    def keyboard_listener(self):
        while rclpy.ok():
            # Wait for user input in the terminal
            user_input = input(
                "Press 's' to START or 'x' to STOP the system: \n")
            if user_input.lower() == 's':
                self.send_enable_request(True)
            elif user_input.lower() == 'x':
                self.send_enable_request(False)

    def send_enable_request(self, enable):
        req = SetProcessBool.Request()
        req.enable = enable

        # Call Motor Service
        if self.cli_motor.wait_for_service(timeout_sec=1.0):
            self.cli_motor.call_async(req)
            self.get_logger().info(
                f"Sent {'START' if enable else 'STOP'} to Motor")
        else:
            self.get_logger().error('Motor service not available')

        # Call Controller Service
        if self.cli_ctrl.wait_for_service(timeout_sec=1.0):
            self.cli_ctrl.call_async(req)
            self.get_logger().info(
                f"Sent {'START' if enable else 'STOP'} to Controller")
        else:
            self.get_logger().error('Controller service not available')

        self.declare_parameter('type', 'sine')
        self.declare_parameter('amplitude', 5.0)

        self.timer = self.create_timer(0.01, self.timer_callback)
        self.start_time = time.time()

    def timer_callback(self):
        msg = Float32()
        t = time.time() - self.start_time
        signal_type = self.get_parameter(
            'type').get_parameter_value().string_value
        amp = self.get_parameter(
            'amplitude').get_parameter_value().double_value

        if signal_type == 'sine':
            msg.data = amp * np.sin(t)
        elif signal_type == 'square':
            msg.data = amp if (np.sin(t) > 0) else -amp
        else:
            msg.data = 10.0

        self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = SetPointGenerator()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
