## Navigation

### Activate Localisation in Webcontrol (Modules)
- Have the **localisation node** active.
- Have the **slam node** inactive.
- **NEVER ACTIVATE THEM TOGETHER**.

### Switch Maps within the Robot
- SSH to `pal@10.42.0.1` and run:
  ```bash
  ros2 service call /map_server/load_map nav2_msgs/srv/LoadMap "map_url: '/home/pal/maps/{MAP_NAME}/{MAP_NAME}.yaml'"
  ```

### Rviz in the Robot's Docker
1. Open the docker terminal, connect to the robot.
2. Run:
   ```bash
   rviz2 -d /opt/pal/$PAL_DISTRO/share/pmb2_2dnav/config/rviz/navigation.rviz
   ```
3. Estimate the pose with **2D Pose Estimate**.
4. Navigate to pose:
   - Press `START` on the joystick to gain control via the map.
   - Send the robot to arbitrary locations with **Nav2 Goal**.
   - Press `START` on the controller to gain back control immediately.

*(Rviz preview)*

## Mapping

### Activate SLAM in Webcontrol (Modules)
- Have the **localisation node** inactive.
- Have the **slam node** active.
- **NEVER ACTIVATE THEM TOGETHER**.

### Create a Map
1. Rviz in the robot's docker:
   - Open the docker terminal, connect to robot.
   - Run:
     ```bash
     rviz2 -d /opt/pal/$PAL_DISTRO/share/pmb2_2dnav/config/rviz/navigation.rviz
     ```
2. Navigate the robot through the place with joystick teleoperation.

### Save the Map within the Robot
- SSH to `pal@10.42.0.1` and run:
  ```bash
  ros2 run nav2_map_server map_saver_cli -f maps/{MAP_NAME}/{MAP_NAME}.yaml