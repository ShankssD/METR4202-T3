#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import JointState 

# Values for prismatic joint, only need two states HIGH and LOW
HIGH = 2
LOW = -2


def set_height_state_callback(req):
    """
    The set height state callback function takes in an argument and checks the vertical direction the
    gripper needs to go and then publishes the Joint state.
    @param: req: A String variable req used to determine whether the gripper need to go up or down.
    """
    #if req.data"UP" publish HIGH to joint2
    if req.data == 'UP':
        VALUE = HIGH
    elif req.data == "DOWN":
        VALUE = LOW

    pub_msg=JointState()
    pub_msg.name = ['joint_2']
    pub_msg.velocity = [1]
    pub_msg.position = [VALUE]   
    pub.publish(pub_msg)
        
if __name__ =='__main__':
    #Initialises node and sets up publisher and subscriber
    rospy.init_node('dropper')
    rospy.loginfo('Dropper has started')
    pub = rospy.Publisher('/desired_joint_states',JointState, queue_size=1)
    rospy.Subscriber('/set_height_state',String, set_height_state_callback)

    rospy.spin()
