# METR4202 Team 3 Project Guide

## Description:
The project requires the team to design and implement a robotic arm for use within an airport to be used to pick up and deliver passengers luggage from a moving conveyor to specified drop zones. The design implemented by the students replicates the functionality of the required but at a smaller scale using blocks and aruco tags.

## Github Link:
All code can be found on the team github:
https://github.com/ShankssD/METR4202-T3

## Team Members:
- Shanker Dorairajan - 44791151
- Tom Atkinson - 45319486
- Hokul Srikanthan - 45286113
- Abdul Wahab Mirza - 45556160
- Will Schwarer - 44818777

## Hardware and Software Used:
Robot Operating Software (ROS): Used for the functionality of the robot, connecting the code to the physical design.
Raspberry Pi: Used as the main system between the Ubuntu OS computer and the robot. 
Visual Studio Code (VSCode): Used for the programming on the Raspberry Pi for ease of use.

## Package Structure:
- ax12a_interface: Stored location for dynamixel launch files.
- dynamixel_interface: Contains all files for the dynamixel. Obtained directly from the dynamixel github.
- project_description: Contains all files for running the project simulation in Gazebo.
- robot_vision: Contains files related to colour detection. Code for colour detection and calibration obtained from https://github.com/uqmvale6/metr4202_color.
- robot_kinematics: Contains the inverse kinematics, trajectory planning and all other motion and judgement based files within this package.
	- Nodes:
		- inverseKinematicsRotation.py
			- Subscriber:
				- /newEffPosition
			- Publishers:
				- /desired_joint_states
		- conveyorTrial.py
			- Subscriber:
				- /fiducial_transforms
			- Publishers:
				- /conveyor_rotation
		- blockTransformPub.py
			- Subscriber:
				- /fiducial_transforms
				-/conveyor_rotation
			- Publishers:
				- /availableBlockTransforms
		- dropper.py
			- Subscriber:
				- /set_height_state
			- Publishers:
				- /desired_joint_states

- sg90_gripper: Contains the files related to the SG90 Gripper inclusive of gripping and releasing the block.
	- Nodes:
		- gripper_actuate.py
			- Subscriber: 
				- gripper_actuate
			- Publisher:
				- gripper_state
- ximea_ros_cam: Contains all files for the Ximea camera. Obtained directly from the Ximea github.
- st_machine: Combines all the code into one working state machine with all logic implemented.
	- Nodes:
		- stm_wait.py
			- Subscriber:
				- /availableBlockTransforms
			- Publisher:
				- /newEffPosition
				- /set_height_state
				- /gripper_actuate

## Launching the Robot:
1. Run the terminal.
2. Using the computer's terminal, SSH to the Raspberry Pi using `ssh metr4202@ip` where the ip would be obtained using `if config` on the Raspberry Pi.
3. Enter into the `catkin_ws` workspace and use `roslaunch robot_kinematics robot_start.launch`.
4. Enter `rosrun st_machine stm_wait.py` in order to start the state machine.
5. Enter `rqt_image_view` in order to view the camera if desired.
6. All files should be launched and the robot should work.
