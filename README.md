# ArUco → ROS 2 → turtlesim Demo

A basic ROS 2 Jazzy demonstration in which a Python/OpenCV camera detects
6x6 ArUco markers and sends their IDs through a ROS 2 topic. A second node
converts the IDs into `/turtle1/cmd_vel` commands for turtlesim.

## Marker mapping

| ID | Action |
|---:|---|
| 1 | Turn left |
| 2 | Move up / forward |
| 3 | Turn right |
| 4 | Move down / backward |
| 5 | Move forward |
| 6 | Move backward |

The first four demonstrate directional/turning behavior. IDs 5 and 6
explicitly demonstrate forward and backward movement.

## Install

Source ROS 2 Jazzy:

```bash
source /opt/ros/jazzy/setup.bash
```

Install ROS dependencies:

```bash
sudo apt update
sudo apt install ros-jazzy-turtlesim ros-jazzy-geometry-msgs ros-jazzy-std-msgs
```

Install OpenCV:

```bash
sudo apt install python3-opencv
```

Check whether the ArUco module and modern API are available:

```bash
python3 -c "import cv2; print(cv2.__version__); print(hasattr(cv2, 'aruco')); print(hasattr(cv2.aruco, 'ArucoDetector'))"
```

If `cv2.aruco` is missing, install an OpenCV build containing the contrib
modules. A virtual environment can be used if your Ubuntu Python installation
prevents pip from modifying the system environment.

## Build

Create a workspace:

```bash
mkdir -p ~/aruco_ws/src
cd ~/aruco_ws/src
```

Copy this package into `~/aruco_ws/src/aruco_turtlesim_demo`.

Then:

```bash
cd ~/aruco_ws
source /opt/ros/jazzy/setup.bash
colcon build --symlink-install
source install/setup.bash
```

## Run

The launch file starts turtlesim, the ArUco detector, and the turtle
controller:

```bash
ros2 launch aruco_turtlesim_demo aruco_turtlesim.launch.py
```

The default camera index is `2`, matching the original OpenCV program.

For another camera:

```bash
ros2 launch aruco_turtlesim_demo aruco_turtlesim.launch.py camera_index:=0
```

## Generate the six markers

The detector uses:

```python
cv2.aruco.DICT_6X6_250
```

Use marker IDs 1, 2, 3, 4, 5, and 6.

For example, print the markers from an ArUco generator and place them in
front of the camera one at a time.

## Test the ROS pipeline without a camera

You can publish marker IDs manually:

```bash
ros2 topic pub --once /aruco_marker_id std_msgs/msg/Int32 "{data: 2}"
```

Try all six:

```bash
ros2 topic pub --once /aruco_marker_id std_msgs/msg/Int32 "{data: 1}"
ros2 topic pub --once /aruco_marker_id std_msgs/msg/Int32 "{data: 2}"
ros2 topic pub --once /aruco_marker_id std_msgs/msg/Int32 "{data: 3}"
ros2 topic pub --once /aruco_marker_id std_msgs/msg/Int32 "{data: 4}"
ros2 topic pub --once /aruco_marker_id std_msgs/msg/Int32 "{data: 5}"
ros2 topic pub --once /aruco_marker_id std_msgs/msg/Int32 "{data: 6}"
```

## Inspect ROS communication

See active nodes:

```bash
ros2 node list
```

Expected nodes include:

```text
/aruco_detector
/turtle_controller
/turtlesim
```

See topics:

```bash
ros2 topic list
```

See marker IDs:

```bash
ros2 topic echo /aruco_marker_id
```

See turtle velocity commands:

```bash
ros2 topic echo /turtle1/cmd_vel
```

Inspect the graph:

```bash
rqt_graph
```

The expected data path is:

```text
Camera
  ↓
aruco_detector
  ↓
/aruco_marker_id
  ↓
turtle_controller
  ↓
/turtle1/cmd_vel
  ↓
turtlesim
```
# aruco_turtlesim_demo
# aruco_turtlesim_demo
