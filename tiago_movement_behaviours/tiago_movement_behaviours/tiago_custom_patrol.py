import rclpy
import random
import yaml
from pathlib import Path
from rclpy.action import ActionClient
from rclpy.node import Node
from nav2_msgs.action import NavigateToPose # Example: Navigation
from action_msgs.msg import GoalStatus
from ament_index_python.packages import get_package_share_directory

class NavActionClient(Node):
    def __init__(self):
        super().__init__('nav_action_client')
        # Create action client
        self._action_client = ActionClient(self, NavigateToPose, '/navigate_to_pose')
        self._wait_timer = None
        self.timer_delay = 10.0  # Seconds to wait after reaching a goal before sending the next one
        default_config_path = str(
            Path(get_package_share_directory('tiago_movement_behaviours'))
            / 'configs'
            / 'goal_waypoints.yaml'
        )
        self.declare_parameter('waypoints_file', default_config_path)
        self._waypoints_file = self.get_parameter('waypoints_file').value
        self._waypoints = self._load_waypoints()

    def _default_waypoints(self):
        return [
            (1.0, 1.0, 0.0, 1.0),
            (2.0, 0.0, 0.0, 1.0),
            (0.0, -1.0, 0.0, 1.0),
            (-1.0, 0.5, 0.0, 1.0),
        ]

    def _load_waypoints(self):
        config_path = Path(self._waypoints_file)
        self.get_logger().info(f'Using waypoint config: {config_path}')

        try:
            with config_path.open('r', encoding='utf-8') as file_handle:
                config = yaml.safe_load(file_handle) or {}
        except Exception as exc:
            self.get_logger().warn(
                f'Could not read waypoint config {config_path}: {exc}. Using defaults.'
            )
            return self._default_waypoints()

        raw_waypoints = config.get('waypoints', [])
        parsed_waypoints = []

        for waypoint in raw_waypoints:
            try:
                parsed_waypoints.append(
                    (
                        float(waypoint['x']),
                        float(waypoint['y']),
                        float(waypoint.get('oz', 0.0)),
                        float(waypoint.get('ow', 1.0)),
                    )
                )
            except Exception:
                self.get_logger().warn(f'Skipping invalid waypoint entry: {waypoint}')

        if not parsed_waypoints:
            self.get_logger().warn('No valid waypoints found in YAML. Using defaults.')
            return self._default_waypoints()

        self.get_logger().info(f'Loaded {len(parsed_waypoints)} waypoints from {config_path}')
        return parsed_waypoints

    def send_goal(self, px, py, oz, ow):
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose.header.frame_id = 'map'
        goal_msg.pose.pose.position.x = px
        goal_msg.pose.pose.position.y = py
        goal_msg.pose.pose.orientation.z = oz
        goal_msg.pose.pose.orientation.w = ow

        # Wait for server
        self._action_client.wait_for_server()

        # Send goal asynchronously
        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg, 
            feedback_callback=self.feedback_callback
        )
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def send_random_goal(self):
        waypoint = random.choice(self._waypoints)
        px, py, oz, ow = waypoint
        self.get_logger().info(
            f'Sending patrol goal to x={px:.2f}, y={py:.2f}'
        )
        self.send_goal(px, py, oz, ow)
    

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            return
        self.get_logger().info('Goal accepted')
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def feedback_callback(self, feedback_msg):
        # Process feedback (e.g., distance remaining)
        self.get_logger().info(f'Feedback: {feedback_msg.feedback.distance_remaining}')

    def get_result_callback(self, future):
        result = future.result()
        if result.status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info('Goal reached. Waiting 10 seconds before next goal.')
        else:
            self.get_logger().warn(
                f'Goal finished with status code {result.status}. Waiting 10 seconds before next goal.'
            )

        if self._wait_timer is not None:
            self._wait_timer.cancel()
        self._wait_timer = self.create_timer(self.timer_delay, self._wait_and_send_next_goal)

    def _wait_and_send_next_goal(self):
        if self._wait_timer is not None:
            self._wait_timer.cancel()
            self._wait_timer = None
        self.send_random_goal()

def main(args=None):
    rclpy.init(args=args)
    action_client = NavActionClient()
    action_client.send_random_goal()
    rclpy.spin(action_client)
    rclpy.shutdown()