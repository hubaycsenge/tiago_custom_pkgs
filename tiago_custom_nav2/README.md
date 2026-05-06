# tiago_custom_nav2

This package provides the ROS 2-based navigation (Nav2) toolkit, customized specifically for the TIAGo (PMB2) robot. It is intended to work instead of the default navigation stack, giving more control over configurations and behavior trees.

## Features
* **Custom Navigation Substitutions**: Replaces the default TIAGo navigation mechanisms with customized Nav2 setups.
* **Custom Behavior Trees**: Includes specialized XML behavior trees (e.g., `navigate_to_pose_w_replanning_and_recovery_w_backup.xml`) designed to handle complex navigation scenarios efficiently.
* **Custom Parameters and Launch Files**: Custom configurations tailored for the TIAGo footprint and sensors, integrated into custom launch profiles.