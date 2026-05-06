# tiago_custom_modules

This package serves as an extension that natively integrates custom ROS 2 nodes and launch files into the TIAGo Webcontrol and command-line module system. This allows custom packages to be managed (started, stopped, restarted) as TIAGo modules using `pal module` tools.

## Available Modules

These modules are defined in the `module/` directory using YAML configuration files. They will appear in the module list with the following names:

* **`custom_navigation`**
  * **Function:** Integrates the custom ROS 2 Nav2 navigation stack (from `tiago_custom_nav2`), allowing it to be managed via the module system in place of the default TIAGo navigation. It also includes the custom noise behaviour implemented when the robot is surrounded.

* **`custom_patrolling`**
  * **Function:** Launches the custom patrolling behavior, sending the robot to randomly navigate between predefined waypoints on the map (for example, utilizing the `patrol_south6th.yaml` configuration).
