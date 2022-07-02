# i-spy
Play the [I Spy] game with the [Kinova Gen3] Robot!

## Main Software/Library Requirements:
- [Ubuntu 18.04.6]
- [ROS Melodic]
  - [rospy]
  - [roslaunch]
  - [smach]
  - [actionlib]
  - [sensor_msgs]
  - [cv_bridge]
- [darknet_ros]
- [ros_kortex_vision]
- [OpenCV]
- [opencv-python] v4.2.0.32
- [SpeechRecognition]
  - [PyAudio]
- [pyttsx3]
  - [espeak]


## Installation

```sh
$ cd ~/catkin_ws/src
$ git clone https://github.com/soroush-msd/i-spy.git
```


## Build

```sh
$ cd ~/catkin_ws/
$ catkin_make
```
## Run

In one terminal:
```sh
$ roscore
```
And in another terminal:
```sh
$ cd ~/catkin_ws/
$ source devel/setup.bash
$ rosrun i-spy stateMachine.py
```

## State Machine Interactions

<img src="https://user-images.githubusercontent.com/83174840/176863533-5570e49f-d987-4cc4-bc51-cee35bc2f47f.png" width="350" height="350" />


  [darknet_ros]: <https://github.com/leggedrobotics/darknet_ros>
  [OpenCV]: <https://docs.opencv.org/4.x/d7/d9f/tutorial_linux_install.html>
  [SpeechRecognition]: <https://pypi.org/project/SpeechRecognition/>
  [pyttsx3]: <https://pypi.org/project/pyttsx3/>
  [cv_bridge]: <http://wiki.ros.org/cv_bridge>
  [smach]: <http://wiki.ros.org/smach>
  [opencv-python]: <https://pypi.org/project/opencv-python/>
  [actionlib]: <http://wiki.ros.org/actionlib>
  [sensor_msgs]: <http://wiki.ros.org/sensor_msgs>
  [roslaunch]: <http://wiki.ros.org/roslaunch/API%20Usage>
  [rospy]: <http://wiki.ros.org/rospy>
  [ROS Melodic]: <http://wiki.ros.org/melodic/Installation/Ubuntu>
  [Ubuntu 18.04.6]: <https://releases.ubuntu.com/18.04/>
  [Kinova Gen3]: <https://www.kinovarobotics.com/product/gen3-robots>
  [ros_kortex_vision]: <https://github.com/Kinovarobotics/ros_kortex_vision>
  [espeak]: <http://espeak.sourceforge.net>
  [PyAudio]: <http://people.csail.mit.edu/hubert/pyaudio/#downloads>
  [I Spy]: <https://en.wikipedia.org/wiki/I_spy>
