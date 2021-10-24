#!/usr/bin/env python

#Import necessary libraries 
import rospy
import pigpio
from std_msgs.msg import String




#Variables for Opened/Closed state of gripper
OPEN_ANGLE =1350
CLOSE_ANGLE= 1530
GRIPPER_STATE="OPEN"

def destination_state_callback(msg):
    """
    The destination state callback function takes in a parameter that tells the gripper what state should be published.
    @param msg: A String message parameter that is read in order to determine the state to be published and angle to be actuated.
    """
    if msg.data=='OPEN':
        #IF msg.data is TRUE then gripper must open and stay opened  until msg.data is false
        pi.set_servo_pulsewidth(servoPin,OPEN_ANGLE)
        GRIPPER_STATE='OPEN'

    else:
        #Once msg.data is FALSE then gripper close
        pi.set_servo_pulsewidth(servoPin,CLOSE_ANGLE)
        GRIPPER_STATE='CLOSE'
    
    pub.publish(GRIPPER_STATE)

if __name__ == '__main__':
    #Sets GPIO pin 12 as an output for the serov
    servoPin =12
    pi = pigpio.pi()
    pi.set_mode(servoPin,pigpio.OUTPUT)

    rospy.init_node('gripper_actuator')
    
    rospy.loginfo('Started Gripper Node')

    #Publishes gripper state to gripper_state
    pub = rospy.Publisher('gripper_state',String,queue_size =10)
    #Subscribes to open_gripper to determine when to open or close
    sub = rospy.Subscriber('gripper_actuate',String,destination_state_callback)
    #Allows for the node to stay open and call backs to be used
    rospy.spin()


