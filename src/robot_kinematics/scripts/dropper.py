#!/usr/bin/env python

import rospy
import numpy as np 
from std_msgs.msg import Bool,String
from sensor_msgs.msg import JointState 

HIGH = 2
LOW = -2
object_gripped = False
def set_height_state_callback(req):
    #if req.data TRUE I.E HIGH publish HIGH to joint2
    if req.data:
        VALUE = HIGH
    else:
        VALUE = LOW

    pub_msg=JointState()
    pub_msg.name = ['joint_2']
    pub_msg.velocity = [1]
    pub_msg.position = [VALUE]   
    pub.publish(pub_msg)
    
    # if VALUE == HIGH:
    #     VALUE=LOW
    # else:
    #     VALUE=HIGH
    #     gripper.publish("CLOSE")
    #     object_gripped = True
    

        

if __name__ =='__main__':
    rospy.init_node('dropper')
    pub = rospy.Publisher('desired_joint_states',JointState, queue_size=1)
    gripper = rospy.Publisher('open_gripper',String,queue_size=1)
    rospy.Subscriber('set_height_state',Bool, set_height_state_callback)

    rospy.spin()