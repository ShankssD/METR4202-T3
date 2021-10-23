#!/usr/bin/env python

import rospy
import numpy as np 
import tf as tf
import modern_robotics as mr
from tf2_msgs.msg import TFMessage
from sensor_msgs.msg import JointState 
from std_msgs.msg import Bool,String

L1 = 0.120 
L2 = 0.095
init_grip_z = 0.15
PRIS_UP = 2
PRIS_DOWN =-2



class inverseKinematics:
    def __init__(self):
        rospy.init_node('inverseKinematics', anonymous = False)
        self.currently_moving = False
        self.pris_state = PRIS_UP
        rospy.Subscriber('/newEffPosition', TFMessage, self.analytical_IK)
        self.gripper_state = "CLOSE"
        self.pub = rospy.Publisher('/desired_joint_states', JointState, queue_size = 1)
        rospy.spin()
        
 

    def analytical_IK(self, msg):
        print(msg.transforms)
        msg = msg.transforms[0]
        x_pos = msg.transform.translation.x +0.05
        y_pos = msg.transform.translation.y +0.05
        z_pos = msg.transform.translation
        quart_xyzw = msg.transform.rotation
        rot_mat = tf.transformations.euler_from_quaternion([quart_xyzw.x, quart_xyzw.y, quart_xyzw.z, quart_xyzw.w])
        print(rot_mat[2])
        theta1,theta3,theta4 = self.required_horiz_joint_angles(x_pos,y_pos, rot_mat[2])
        if theta1 == 'no solution found':
            print('NSF')
            
            return None
        
        pub_msg = JointState()
        pub_msg.name = ['joint_1','joint_3', 'joint_4']
        pub_msg.velocity = [1,1,1]
        pub_msg.position = [theta1,theta3,theta4]
        
        if(not self.currently_moving):
            self.pub.publish(pub_msg)

        
        

        

        


        
    def required_horiz_joint_angles (self, x,y, rot_rel_base):
        max_reach_fwd = L1 + L2 
        max_reach_bck = L1 - L2 
        print(np.sqrt(x**2 + y**2), x,y)
        if( np.sqrt(x**2 + y**2) < max_reach_bck or np.sqrt(x**2 + y**2) > max_reach_fwd ):
            
            return ("no solution found","no solution found", "no solution found")
        else:
            beta = np.arccos((L1**2 + L2**2 - x**2 -y**2)/(2*L1*L2))
            alpha = np.arccos((x**2 + y**2 + L1**2 -L2**2)/(2*L1*np.sqrt(x**2 + y**2)))
            gamma = np.arctan2(y,x)

            theta1 = gamma - alpha
            theta2 = np.pi - beta
            print("Before, ",theta1*180/np.pi, theta2*180/np.pi)

            theta2 = -theta2
            theta3 = rot_rel_base + (theta1 + theta2)

            if theta1<-1:
                theta1+=2*np.pi

            return (theta1,theta2,theta3)

    
    


if __name__ == '__main__':
    node = inverseKinematics()
