#!/usr/bin/env python

#Import necessary libaries 
from gpiozero import AngularServo
import rospy
from std_msgs.msg import String
#Creates AngularServo class, on pin 23 specifying the desired max and min angles
gripper = AngularServo(23,min_angle=-90,max_angle=90)
#Variables for Opened/Closed state of gripper
OPEN_ANGLE =-65
CLOSE_ANGLE= 0
GRIPPER_STATE="OPEN"
gripper.angle=OPEN_ANGLE
def destination_state_callback(msg):
    if msg.data=='OPEN':
        #IF msg.data is TRUE then gripper must open and stay opened  until msg.data is false
        gripper.angle=OPEN_ANGLE
        GRIPPER_STATE='OPEN'

    else:
        #Once msg.data is FALSE then gripper close
        gripper.angle=CLOSE_ANGLE
        GRIPPER_STATE='CLOSE'
    
    pub.publish(GRIPPER_STATE)
if __name__ == '__main__':
    rospy.init_node('gripper_actuator')
    #Publishes gripper state to gripper_state
    pub = rospy.Publisher('gripper_state',String,queue_size =10)
    #Subscribes to open_gripper to determine when to open or close
    sub = rospy.Subscriber('actuate_gripper',String,destination_state_callback)
    #Allows for the node to stay open and call backs to be used
    rospy.spin()


