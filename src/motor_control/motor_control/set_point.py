import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
import numpy as np # NumPy is allowed [cite: 121, 188]
import time

class SetPointGenerator(Node):
    def __init__(self):
        super().__init__('sp_gen')
        self.publisher_ = self.create_publisher(Float32, '/set_point', 10)
        
        # Extension: Parameter to change signal type at runtime [cite: 187]
        # Types: 'constant', 'sine', 'square'
        self.declare_parameter('type', 'sine') 
        self.declare_parameter('amplitude', 5.0)
        
        # Timer matching the system sample time (0.01s) [cite: 96, 115]
        self.timer = self.create_timer(0.01, self.timer_callback)
        self.start_time = time.time()

    def timer_callback(self):
        msg = Float32()
        t = time.time() - self.start_time
        
        # Get current parameter values
        signal_type = self.get_parameter('type').get_parameter_value().string_value
        amp = self.get_parameter('amplitude').get_parameter_value().double_value

        # Extension: Logic for different signal types [cite: 184, 185]
        if signal_type == 'sine':
            msg.data = amp * np.sin(t)
        elif signal_type == 'square':
            msg.data = amp if (np.sin(t) > 0) else -amp
        else: # Default Constant
            msg.data = 10.0 # Your current setpoint goal

        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = SetPointGenerator()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()