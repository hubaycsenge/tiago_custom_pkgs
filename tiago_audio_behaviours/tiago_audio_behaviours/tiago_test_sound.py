import rclpy
from rclpy.node import Node
from audio_common_msgs.msg import AudioData
import os
from ament_index_python.packages import get_package_share_directory

class SoundPublisher(Node):
    def __init__(self):
        super().__init__('sound_publisher')
        self.publisher_ = self.create_publisher(AudioData, '/audio', 10)
        
        # Change the default parameter to look for the MP3 file
        self.declare_parameter('sound_file', 'greet1.mp3')
        sound_file_name = self.get_parameter('sound_file').get_parameter_value().string_value
        
        pkg_share = get_package_share_directory('tiago_audio_behaviours')
        self.sound_file_path = os.path.join(pkg_share, 'soundfiles', sound_file_name)
        
        if not os.path.exists(self.sound_file_path):
            self.get_logger().error(f'Sound file not found: {self.sound_file_path}')
            self.file_stream = None
            return
            
        self.get_logger().info(f'Loaded sound file: {self.sound_file_path}')
        
        # Open the MP3 file as raw binary
        self.file_stream = open(self.sound_file_path, 'rb')
        self.chunk_size = 4096
        
        self.timer = self.create_timer(0.1, self.timer_callback)

    def timer_callback(self):
        if self.publisher_.get_subscription_count() == 0:
            self.get_logger().info('Waiting for audio subscriber...', throttle_duration_sec=2.0)
            return

        if not self.file_stream:
            return
            
        data = self.file_stream.read(self.chunk_size)
        if not data:
            self.get_logger().info('End of sound file reached.')
            self.timer.cancel()
            self.file_stream.close()
            self.file_stream = None
            return
            
        msg = AudioData()
        msg.data = list(data)
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = SoundPublisher()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
        
    if getattr(node, 'file_stream', None):
        node.file_stream.close()
        
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()