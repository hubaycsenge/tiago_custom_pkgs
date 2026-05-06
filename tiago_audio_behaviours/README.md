# tiago_audio_behaviours

This ROS2 package contains nodes for audio handling in specific cases for the TIAGo robot.

## Features currently implemented
* **Tester Node (`tiago_test_sound.py`)**: A simple node developed to test audio playback capabilities.
* **Navigation Recovery Sound Node (`tiago_nav_recov_sound.py`)**: A navigation-dependent node that emits warning noises if the robot is being surrounded (e.g., in a crowd) and cannot exit, serving as an audio cue during navigation recoveries.
