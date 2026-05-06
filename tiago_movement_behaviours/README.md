# tiago_movement_behaviours

This ROS2 package contains various high-level, navigation-focused behaviors for the TIAGo robot.

## Features currently implemented
* **Patrolling Behavior (`tiago_custom_patrol.py`)**: A behavior intended to automate area surveillance or general random walks. It expects a configuration file with a set of places/waypoints on a given map and continuously sends the robot to navigate randomly between these points. Configurations can be adjusted in the `configs/` directory.