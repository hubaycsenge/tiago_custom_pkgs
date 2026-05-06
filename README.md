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

Deploying  #TODO: add link

---

Web Control Setup

### Starting Web Control Services

After SSH into robot (`ssh pal@10.42.0.1`), run these commands in **separate terminals**:

**Terminal 1 — Rosbridge WebSocket:**
```bash
source /home/pal/deployed_ws/setup.bash
ros2 launch rosbridge_server rosbridge_websocket_launch.xml call_services_in_new_thread:=True send_action_goals_in_new_thread:=True
```

**Terminal 2 — FerretDB (database):**
```bash
/opt/pal/alum/lib/webgui_ferretdb_cfg/webgui_ferretdb
```

**Terminal 3 — WebGUI ROS2 Utils Node:**
```bash
source /home/pal/deployed_ws/setup.bash
/opt/pal/alum/lib/webgui_ros2_utils/webgui_ros2_utils_node
```

**Terminal 4 (optional — usually already running):**
```bash
source /home/pal/deployed_ws/setup.bash
/opt/venvs/webgui/webgui-rest-server/bin/gunicorn 'webgui_rest_server.main:run_app()' --workers=2 --worker-class=uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Accessing Web UI

Open in browser:
```
http://10.42.0.1:3003
```

**Service Ports:**
- Web UI: `3003`
- Rosbridge WebSocket: `9090`
- REST API: `8000`
- FerretDB: `127.0.0.1:27017`

---
