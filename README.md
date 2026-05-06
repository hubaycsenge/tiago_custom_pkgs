# Repository for custom ROS2 packages for Tiago PMB2 base

## packages 

### tiago_custom_nav2
Contains custom Nav2 configurations, custom behavior trees (BTs) for robust navigation (incorporating replanning, backup, and recovery routines), and customized launch files replacing the default TIAGo navigation stack.

### tiago_audio_behaviours
Manages audio playback and sound effects for the robot. This includes playing audio notifications during navigation recoveries and publishing `.wav` file chunks as `AudioData` over ROS topics.

### tiago_custom_modules
Holds custom PMB2 / TIAGo module and configuration integrations, such as `00_custom_navigation.yaml`, used to load custom navigation settings into the robot's default execution modules.

### tiago_movement_behaviours
Contains automated routines and behaviors for robot movement. Includes configurable YAML waypoints (for dstinct floor layouts/departments) and scripts to drive the TIAGo robot through predefined navigation paths autonomously, such as patrol tasks.

## Know-how

The comprehensive documentation has been split into several focused guides:

* [Basic operation](documentation/Basic_functions.md) (Bringup, Turnoff,Charging, Teleoperation, Pal Module Operations)
* [Connection](documentation/Connection.md) (SSH, SSHFS, Docker)
* [Webcontrol](documentation/Connection.md) (Webcontrol startup, with or without docker)
* [Navigation and Mapping](documentation/Nav_and_mapping.md) (Localization, SLAM, Map Switching, and RViz)
* [Contributing](documentation/Contributing.md) (Deploy new ROS2 nodes, Pal modules)

## Official Documentation

For further reference regarding the PMB2 base and the robot's software architecture, please consult the official documents:

* [PMB2 Handbook](https://docs.pal-robotics.com/tiago-base/handbook.html#)
* [PAL SDK (Robot's Custom Software System)](https://docs.pal-robotics.com/sdk/23.12/)

