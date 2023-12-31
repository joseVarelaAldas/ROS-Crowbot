# ROS-Crowbot
To use this tool noetic ROS with python dependencies is required.
# Preparation
Upload the arduino program to the Crowbot robot (install the necessary libraries and setup network data).

Install rosserial for ubuntu 20.04 (noetic).
```
sudo apt-get install ros-noetic-rosserial
```
Run the rosmaster.
```
roscore
```
Run rosserial TCP bridge (new terminal).
```
rosrun rosserial_python serial_node.py tcp
```
Testing code o run examples.
# Testing
To control the RGB LEDs.
```
rostopic pub /Leds std_msgs/Int32MultiArray "layout:
  dim:
  - label: ''
    size: 0
    stride: 0
  data_offset: 0
data:
- 0
- 0
- 0"
```
To control the movements of the robot (linear X and angular Z).
```
rostopic pub /Control geometry_msgs/Twist "linear:
  x: 0.0
  y: 0.0
  z: 0.0
angular:
  x: 0.0
  y: 0.0
  z: 0.0"
```
To control the buzzer.
```
rostopic pub /Buzzer  std_msgs/Bool "data: true"
```
To read sensors (Example with distance).
```
rostopic echo /Distance
```
# Examples
The examples have been created with Visual Studio Code.

CrowControl1.

[![Alt text](https://img.youtube.com/vi/5j4wBaW1kaM/0.jpg)](https://www.youtube.com/watch?v=5j4wBaW1kaM)

CrowControl2

[![Alt text](https://img.youtube.com/vi/xRhDtNmLW4Y/0.jpg)](https://www.youtube.com/watch?v=xRhDtNmLW4Y)
