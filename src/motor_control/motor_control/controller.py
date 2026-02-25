import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
import numpy as np # Only NumPy is allowed [cite: 121]

class PIDController(Node):
    def __init__(self):
        super().__init__('ctrl') # Node name must be /ctrl [cite: 117]
        
        # Declare parameters for tuning at runtime [cite: 126, 127]
        self.declare_parameter('kp', 0.2)
        self.declare_parameter('ki', 2.0)
        self.declare_parameter('kd', 0.0)
        self.declare_parameter('ts', 0.01) # Sampling time [cite: 115]

        # Publishers and Subscribers [cite: 125]
        self.sub_sp = self.create_subscription(Float32, '/set_point', self.sp_callback, 10)
        self.sub_mv = self.create_subscription(Float32, '/motor_output_y', self.mv_callback, 10)
        self.pub_u = self.create_publisher(Float32, '/motor_input_u', 10)

        # Variables for PID logic [cite: 158]
        self.set_point = 0.0
        self.motor_output = 0.0
        self.error_integral = 0.0
        self.prev_error = 0.0
        
        # Timer for control loop [cite: 115]
        ts = self.get_parameter('ts').get_parameter_value().double_value
        self.timer = self.create_timer(ts, self.control_loop)

    def sp_callback(self, msg):
        self.set_point = msg.data

    def mv_callback(self, msg):
        self.motor_output = msg.data

    def control_loop(self):
        # Fetch current gains 
        kp = self.get_parameter('kp').value
        ki = self.get_parameter('ki').value
        kd = self.get_parameter('kd').value
        ts = self.get_parameter('ts').value

        # PID Math [cite: 157, 158]
        error = self.set_point - self.motor_output
        self.error_integral += error * ts
        error_der = (error - self.prev_error) / ts
        
        u = (kp * error) + (ki * self.error_integral) + (kd * error_der)
        
        # Publish control signal
        msg = Float32()
        msg.data = float(u)
        self.pub_u.publish(msg)
        
        self.prev_error = error

def main():
    rclpy.init()
    node = PIDController()
    rclpy.spin(node)
    rclpy.shutdown()