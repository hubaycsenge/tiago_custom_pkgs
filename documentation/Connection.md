## Connection with Laptop

### Docker – For Navigation and Webcontrol Access
1. In a terminal:
   ```bash
   docker start -ai pmb2-61-dev
   ```
2. In the newly opened black terminal:
   ```bash
   pal connection start
   ```
   - **IP:** `10.42.0.1`
   - **Start automatic:** `y`
   - **ROS domain ID:** `1`

*(Starting the docker – a normal state screenshot)*


### SSH – For Getting the Robot's Actual Terminal
Useful for saving and loading maps.
- New terminal: 
  ```bash
  ssh pal@10.42.0.1
  ```

### SSHFS – Reaching the Robot's File System
Useful for easier file transfer.
- New terminal: 
  ```bash
  sshfs pal@10.42.0.1:/ /root/pal_drive
  ```
- This opens the robot's whole file system in a new folder at `/root/pal_drive`.
