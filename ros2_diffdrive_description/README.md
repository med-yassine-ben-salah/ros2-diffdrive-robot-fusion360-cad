# `ros2_diffdrive_description` — ROS 2 URDF & Xacro Package (RViz2 + Gazebo + `ros2_control`)

Generated directly from the verified FreeCAD assembly (`ROS2_DiffDrive_Robot.FCStd`) with full feature parity against `my_bot` (`model.urdf.xacro`).
All meshes in `meshes/*.stl` are scaled to **metres (`× 0.001`)** and shifted to their exact kinematic link origins.

## 1. TF Frame Tree & Kinematic Origins (REP-103 / REP-105 + `my_bot` Node Compatibility)

| Frame / Link | Parent | Joint Type | Origin Relative to Parent (`x, y, z` m) | World Position (`X, Y, Z` mm) | Description |
|---|---|---|---|---|---|
| `base_footprint` | — | — | `(0.000, 0.000, 0.000)` | `(0.0, 0.0, 0.0)` | Ground plane projection under rear drive axle midpoint |
| `base_link` | `base_footprint` | `fixed` | `(0.000, 0.000, 0.0325)` | `(0.0, 0.0, 32.5)` | Rear drive wheel axle midpoint |
| `left_wheel_link` | `base_link` | `continuous` (`+Y`, damping `0.01`) | `(0.000, +0.0895, 0.000)` | `(0.0, +89.5, 32.5)` | Left 65 mm drive wheel (`wheel_separation = 0.1790 m`, `wheel_radius = 0.0325 m`) |
| `right_wheel_link` | `base_link` | `continuous` (`+Y`, damping `0.01`) | `(0.000, -0.0895, 0.000)` | `(0.0, -89.5, 32.5)` | Right 65 mm drive wheel |
| `left_motor_link` | `base_link` | `fixed` | `(0.000, +0.0365, 0.000)` | `(0.0, +36.5, 32.5)` | Left JGA25-370 geared DC motor + encoder |
| `right_motor_link` | `base_link` | `fixed` | `(0.000, -0.0365, 0.000)` | `(0.0, -36.5, 32.5)` | Right JGA25-370 geared DC motor + encoder |
| `caster_link` | `base_link` | `fixed` | `(0.165, 0.000, -0.0245625)` | `(165.0, 0.0, 7.9375)` | Front 5/8" (`15.875 mm`) steel ball caster (frictionless `mu1=0, mu2=0` in Gazebo) |
| `battery_door_link` | `base_link` | `revolute` (`+Z`, `0..1.5708 rad / 90°`) | `(0.107, -0.0736, 0.0045)` | `(107.0, -73.6, 37.0)` | Snap-fit pivot hinge side door with cantilever latch lock |
| `imu_link` | `base_link` | `fixed` | `(0.055, 0.000, 0.03664)` | `(55.0, 0.0, 69.14)` | `MPU9250` 9-axis IMU at exact support-triangle centroid (`+X` fwd, `+Y` left, `+Z` up) |
| `lidar_link` | `base_link` | `fixed` | `(0.000, 0.000, 0.08675)` | `(0.0, 0.0, 119.25)` | `LDS02RR` 360° laser scanner head (collinear with rear axle midpoint) |
| `laser_frame` | `lidar_link` | `fixed` | `(0.000, 0.000, 0.000)` | `(0.0, 0.0, 119.25)` | Alias frame for `lidar_link` |
| `camera_link` | `base_link` | `fixed` | `(0.1945, 0.000, 0.066)` | `(194.5, 0.0, 98.5)` | Front `ESP32-CAM` lens center (`+X` forward) |
| `camera_optical_link` | `camera_link` | `fixed` | `rpy=(-π/2, 0, -π/2)` | `(194.5, 0.0, 98.5)` | Standard ROS 2 optical camera frame (`+Z` forward, `+X` right, `+Y` down) |

## 2. Xacro Arguments & `ros2_control` / Gazebo Integration

`urdf/ros2_diffdrive_robot.urdf.xacro` supports the same Xacro arguments as `my_bot`:

- `use_ros2_control` (default `true`):
  - When `true` and `use_sim:=false`: loads `my_bot_hardware/MyBotSystem` (`ticks_per_rev=1400`, `wheel_radius=0.0325`, `wheel_separation=0.1790`, `/left_motor_ticks`, `/right_motor_ticks`, `/cmd_vel`).
  - When `true` and `use_sim:=true`: loads `gazebo_ros2_control/GazeboSystem` + `libgazebo_ros2_control.so` with `config/my_bot_controllers.yaml`.
  - When `false`: falls back to Gazebo `libgazebo_ros_diff_drive.so` + `libgazebo_ros_joint_state_publisher.so`.
- `use_sim` (default `false`): switches between hardware and Gazebo `ros2_control` plugin.
- `publish_odom_tf` (default `true`): controls whether legacy `libgazebo_ros_diff_drive.so` publishes the `odom -> base_footprint` TF directly (set `false` when using `robot_localization` EKF).

Gazebo sensor plugins included:
- **IMU (`imu_link`)**: `libgazebo_ros_imu_sensor.so` (`30 Hz`, remapped to `/imu`, `initial_orientation_as_reference=false`)
- **360° LiDAR (`lidar_link`)**: `libgazebo_ros_ray_sensor.so` (`15 Hz`, `360` samples, `0.05..3.5 m`, Gaussian noise `σ = 0.005 m`, remapped to `/scan`, `frame_name=lidar_link`)
- **Front Camera (`camera_link`)**: `libgazebo_ros_camera.so` (`30 Hz`, `640×480` `R8G8B8`, `FOV = 65°`, `frame_name=camera_optical_link`)

## 3. Quick Start in ROS 2 (Humble / Iron / Jazzy)

```bash
# Copy or symlink ros2_diffdrive_description into your colcon workspace src/ folder:
cd ~/ros2_ws
colcon build --packages-select ros2_diffdrive_description
source install/setup.bash

# Launch Robot State Publisher, Joint State Publisher GUI, and RViz2:
ros2 launch ros2_diffdrive_description display.launch.py

# Optional Xacro arguments:
ros2 launch ros2_diffdrive_description display.launch.py use_ros2_control:=true use_sim:=false
```
