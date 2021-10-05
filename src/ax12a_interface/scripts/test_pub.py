#! /usr/bin/env python
import rospy
from sensor_msgs.msg import JointState

rospy.init_node('test_publisher')
pub = rospy.Publisher('/desired_joint_states',JointState, queue_size=10)
rate = rospy.Rate(10)


msg = JointState()
msg.name = ['joint_1','joint_2','joint_3','joint_4']
msg.velocity = [0.5,0.5,0.5,0.5]
#msg.effort = [0, 0, 0, 0]
position = msg.position
angle = 1.50
direction= -1

while not rospy.is_shutdown():
    msg.position = [angle,angle,angle,angle]
    pub.publish(msg)
    
    if angle < -1.50 :
        direction = 1
    elif angle > 1.50 :
        direction = -1
    
    angle += direction * 0.1
    
    rate.sleep()



