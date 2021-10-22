#!/usr/bin/env python

import rospy
import numpy as np 
import tf as tf
import modern_robotics as mr
from tf2_msgs.msg import TFMessage
from sensor_msgs.msg import JointState 

L1 = 0.120 
L2 = 0.095
init_grip_z = 0.15
HIGH = 2
LOW = -2

class inverseKinematics:
    def __init__(self):
        rospy.init_node('inverseKinematics', anonymous = False)
        rospy.Subscriber('newEffPosition', TFMessage, self.analytical_IK)

        self.pub = rospy.Publisher('desired_joint_states', JointState, queue_size = 1)
        rospy.spin()

    def analytical_IK(self, msg):
        print(msg.transforms)
        msg = msg.transforms[0]
        x_pos = msg.transform.translation.x
        y_pos = msg.transform.translation.y
        z_pos = msg.transform.translation.z
        
        quart_x = msg.transform.rotation.x
        quart_y = msg.transform.rotation.y
        quart_z = msg.transform.rotation.z

        x_eul, y_eul, z_eul = tf.transformations.euler_from_quaternion([quart_x, quart_y, quart_z])

        theta1,theta2 = self.required_horiz_joint_angles(x_pos,y_pos)
        if theta1 == 'no solution found':
            print('NSF')
            return None
        pub_msg = JointState()
        pub_msg.name = ['joint_1','joint_3']
        pub_msg.velocity = [1,1]
        pub_msg.position = [theta1, theta2]
        self.pub.publish(pub_msg)
    
    def required_horiz_joint_angles (self, x,y):
        max_reach_fwd = L1 + L2
        max_reach_bck = L1 - L2
        if( np.sqrt(x**2 + y**2) < max_reach_bck or np.sqrt(x**2 + y**2) > max_reach_fwd ):
            
            return ("no solution found","no solution found")
        else:
            beta = np.arccos((L1**2 + L2**2 - x**2 -y**2)/(2*L1*L2))
            alpha = np.arccos((x**2 + y**2 + L1**2 -L2**2)/(2*L1*np.sqrt(x**2 + y**2)))
            gamma = np.arctan2(y,x)
            
            theta1 = gamma - alpha
            theta2 = np.pi - beta
            if theta1<-1:
                theta1+=2*np.pi
            elif theta1>4:
                theta1-=2*np.pi

            print(theta1,theta2)
            return (theta1,theta2)
    
    def get_prismatic_joint_angle (self, height_reqd, current_joint_angle):
        spool_diam  = (27.3**10^(-3))
        dz = z_pos - init_grip_z
        theta4 = theta1 + theta2 - (z_eul - np.pi/2)
        prismatic_rot = (2*dz)/spool_diam #Rack and pinion formula
        if(theta4 < -2*np.pi or theta4 > -2*np.pi): #will have to tune this to the current setup
            print("Prismatic distance too low")
            return
        else:
            return (theta4)


if __name__ == '__main__':
    node = inverseKinematics()
