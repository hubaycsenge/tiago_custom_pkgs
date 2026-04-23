#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from nav2_msgs.msg import BehaviorTreeLog
from audio_common_msgs.msg import AudioData
import os
import math
import time
from ament_index_python.packages import get_package_share_directory
from nav2_msgs.action import NavigateToPose

class NavRecoveryAudioAlertNode(Node):
    def __init__(self):
        super().__init__('nav_recovery_audio_alert_node')

        # --- Configuration Parameters ---
        self.declare_parameter('danger_distance_m', 0.5)
        self.declare_parameter('danger_distance_perc', 0.3) # Percentage of scan points that must be too close to trigger
        self.declare_parameter('recov_num_threshold', 3) # Number of recoveries that must be active to trigger
        self.declare_parameter('beep_cooldown_s', 3.0)
        self.declare_parameter('sound_file', 'attention1.mp3') # Change to your preferred file
        
        self.danger_distance_m = self.get_parameter('danger_distance_m').value
        self.danger_distance_perc = self.get_parameter("danger_distance_perc").value
        self.beep_cooldown_s = self.get_parameter('beep_cooldown_s').value
        self.recov_num_threshold = self.get_parameter('recov_num_threshold').value
        sound_file_name = self.get_parameter('sound_file').value

        # --- Audio File Setup ---
        try:
            pkg_share = get_package_share_directory('tiago_audio_behaviours')
            self.sound_file_path = os.path.join(pkg_share, 'soundfiles', sound_file_name)
        except Exception as e:
            self.get_logger().error(f"Could not find package share directory: {e}")
            self.sound_file_path = ""

        # State variables
        self.distance_danger_crit = False
        self.recov_crit = False
        self.recov_num = None
        self.active_recoveries = set()
        self.last_beep_time = 0.0
        
        # Audio streaming variables
        self.file_stream = None
        self.chunk_size = 4096

        # --- Publishers & Subscribers ---
        self.audio_pub = self.create_publisher(AudioData, '/audio', 10)

        self.scan_sub = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            rclpy.qos.qos_profile_sensor_data)
        # --- Timers ---
        # 1. Timer to evaluate distance and recovery state (runs at 2 Hz)
        self.eval_timer = self.create_timer(0.5, self.evaluate_and_warn)
        # 2. Timer to stream audio chunks (runs at 10 Hz)
        self.audio_timer = self.create_timer(0.1, self.audio_stream_callback)
        
        self.get_logger().info(f"Audio Alert Node started. Danger threshold: {self.danger_distance_m} m ; {self.recov_num_threshold} recoveries")

        feedback_msg_type = NavigateToPose.Impl.FeedbackMessage
        
        # Subscribe directly to the action's feedback topic
        self.subscription = self.create_subscription(
            feedback_msg_type,
            '/navigate_to_pose/_action/feedback',
            self.feedback_callback,
            10 # QoS profile depth
        )
        self.get_logger().info("Listening to Nav2 feedback...")
    
    def feedback_callback(self, msg):
        # The actual feedback data is nested inside the 'feedback' attribute 
        # of the wrapper message.
        actual_feedback = msg.feedback
        
        self.recov_num = actual_feedback.number_of_recoveries
        if self.recov_num >= self.recov_num_threshold:
            self.recov_crit = True
        else:
            self.recov_crit = False

    def scan_callback(self, msg):
        valid_ranges = [r for r in msg.ranges if msg.range_min < r < msg.range_max and not math.isinf(r) and not math.isnan(r)]
        if valid_ranges:
            num_valid = len(valid_ranges)
            num_too_close = sum(1 for r in valid_ranges if r < self.danger_distance_m)
            self.perc = num_too_close/num_valid
            #self.get_logger().info(f'Num too close: {num_too_close}, num valid: {num_valid} percentage: {perc} danger dist perc: {self.danger_distance_perc}')
            if self.perc > self.danger_distance_perc:
                self.distance_danger_crit = True
            else:
                self.distance_danger_crit = False



    def evaluate_and_warn(self):
        self.get_logger().info(f'Dist percentages: {self.perc}; recoveries: {self.recov_num}')
        if self.distance_danger_crit and self.recov_crit:
            self.get_logger().warn('BEEEEP BEEP')
            current_time = time.time()
            
            # Trigger audio if cooldown passed AND audio isn't already playing
            if (current_time - self.last_beep_time) > self.beep_cooldown_s and self.file_stream is None:
                self.start_audio()
                self.last_beep_time = current_time

    def start_audio(self):
        if not os.path.exists(self.sound_file_path):
            self.get_logger().error(f'Sound file not found: {self.sound_file_path}')
            return
            
        # Open the file. The audio_timer will automatically pick this up and start streaming.
        self.file_stream = open(self.sound_file_path, 'rb')

    def audio_stream_callback(self):
        # If there's no open file stream, do nothing
        if not self.file_stream:
            return
            
        data = self.file_stream.read(self.chunk_size)
        
        # If we reach the end of the file
        if not data:
            self.file_stream.close()
            self.file_stream = None # Reset the stream so evaluate_and_warn can trigger it again later
            return
            
        # Stream the chunk
        msg = AudioData()
        msg.data = list(data)
        self.audio_pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = NavRecoveryAudioAlertNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        # Cleanup the file stream if it was open during a crash/shutdown
        if getattr(node, 'file_stream', None):
            node.file_stream.close()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()