# Repository for custom ROS2 packages for Tiago PMB2 base

## packages 

### tiago_custom_nav2

### tiago_audio_behaviours

### tiago_custom_modules

### tiago_movement_behaviours

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
