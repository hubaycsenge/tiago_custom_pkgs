# Contributing and Development

## Developing ROS2 Packages
The development of the custom ROS2 packages in this repository follows the standard ROS 2 Humble guidelines and syntax. 
For a complete overview of creating and building packages, refer to the official documentation:
[How-To-Guides: Developing a ROS 2 Package](https://docs.ros.org/en/humble/How-To-Guides/Developing-a-ROS-2-Package.html)

## PAL Module Integration
If you are developing a feature that should be manageable via the robot's `pal module` system, you need to register it.
Integration happens by including a `.yaml` file describing the new module in the `module/` directory of the `tiago_custom_modules` package.

## Deployment to the Robot
Once your packages are developed and tested, the final step is to deploy them to the physical robot.

### 1. Enter the Docker Environment and Connect
From your local machine, start and enter the Docker environment, then establish a connection with the robot:
```bash
docker start -ai pmb2-61-dev
pal connection start
```

### 2. Deploy the Code
Navigate to your workspace where the source code resides:
```bash
cd exchange/ros_ws
```
Then, initiate the deployment:
```bash
ros2 run pal_deploy deploy --user pal 10.42.0.1
```
This process structures and places all the necessary software into the `$HOME/deployed_ws` folder on the robot, satisfying the requirements of the robot's existing system.

### 3. Source the Workspace on the Robot
To use your deployed packages, log into the robot via SSH and source the new workspace:
```bash
ssh pal@10.42.0.1
source deployed_ws/setup.bash
```

> **Important Note:** If a custom PAL module was created or modified, it will only become visible to the system *after rebooting the robot*.