# i-spy
Play the [I Spy] game with the [Kinova Gen3] Robot!

## Main Software Requirements:
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

## Build

```sh
$ cd ~/catkin_ws/src
$ git clone https://github.com/soroush-msd/i-spy.git
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
$ rosrun i-spy stateMachine.py [f]emale/[m]ale [h]uman/[r]obot/[g]reeting
```
## How To Play?
This is a voice-based interaction. You need to have three components connected to your system:
- A microphone through which you will speak to the robot.
- A speaker through which the robot will speak to you.
- The Kinova Gen3 Robotic Arm with a working camera to enable the robot to see and detect objects in the environment.

There are two/three-ish different scenarios you can play the game:
1. The robot looks around, chooses one random object, picks its first letter and then you will need to guess the matching object.
2. You look around, choose one random object within the robot's FOV and pick its first letter. The robot then asks you for the letter and tries to guess the matching object.
3. The robot greets you, introduces itself, and then starts scenario 1.


So, for example, if you run:
```sh
$ rosrun i-spy stateMachine.py f r
```
The robot will play scenario 1 with the female voice.
> Note: `f` stands for female, and `r` stands for robot in the command line arguments. This means the robot will have a female voice and will be providing a letter for the user to guess.

Or, if you run:
```sh
$ rosrun i-spy stateMachine.py m h
```
The robot will play scenario 2 with the male voice.
> Note: `m` stands for male, and `h` stands for human in the command line arguments. This means the robot will have a female voice, and you will be providing a letter for the robot to guess.

Similarly, if you run:
```sh
$ rosrun i-spy stateMachine.py m g
```
The robot will play scenario 3 with the male voice.
> Note: `g` stands for greeting in the command line arguments. Refer to scenario 3 for the explanation.


## Important Notes:
:warning: Your microphone needs to remain mute except when you are required to speak to the robot. When ready to speak:
1. Unmute the microphone,
2. Provide input, 
3. Mute back the microphone.

This might be due to the sensitivity of different microphones and the variety of energy level thresholds needed to adjust to ambient noise.\
\
\
:warning: When the robot asks you about the first letter of the object, you need to provide input by speaking in the following format:
- `letter x`, for example, if the object starts with `x`. Or
- `letter y`, for example, if the object starts with `y`.

## State Machine Interactions
The diagram below demonstrates the interactions and transitions between state machines in different stages during the game:

<img src="https://user-images.githubusercontent.com/83174840/176863533-5570e49f-d987-4cc4-bc51-cee35bc2f47f.png" width="350" height="350" />

## Demo Videos
The videos below demonstrate the interactions between a human participant and the robot playing the game in different scenarios.

**Scenario 3 with female voice**\
Related command:
```sh
$ rosrun i-spy stateMachine.py f g
```
https://user-images.githubusercontent.com/83174840/232294901-599f0393-e303-4b49-bb6e-8f8d5d14eb50.mp4


\
\
**Scenario 2 with female voice**\
Related command:
```sh
$ rosrun i-spy stateMachine.py f h
```
https://user-images.githubusercontent.com/83174840/232299016-5fbcb934-582c-48cf-b23b-275ca0bae160.mp4


\
\
**Scenario 1 with male voice**\
Related command:
```sh
$ rosrun i-spy stateMachine.py m r
```
https://user-images.githubusercontent.com/83174840/232307693-9cffd87c-36ae-4417-812c-d43104828ce0.mp4


\
\
**Scenario 2 with male voice**\
Related command:
```sh
$ rosrun i-spy stateMachine.py m h
```
https://user-images.githubusercontent.com/83174840/232307703-21f5c09a-1dc2-4fcf-a26a-3b28b7200271.mp4



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
