#!/usr/bin/env python

import rospy
import numpy as np 
import tf as tf
import modern_robotics as mr
from tf2_msgs.msg import TFMessage
from sensor_msgs.msg import JointState 
from std_msgs.msg import Bool

L1 = 0.120 
L2 = 0.095
init_grip_z = 0.15


class inverseKinematics:
    def __init__(self):
        rospy.init_node('inverseKinematics', anonymous = False)
        rospy.Subscriber('newEffPosition', TFMessage, self.analytical_IK)

        self.pub = rospy.Publisher('desired_joint_states', JointState, queue_size = 1)
        self.height = rospy.Publisher('set_height_state',Bool,queue_size =1)
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

        self.height.publish(False)


        
    def required_horiz_joint_angles (self, x,y):
        max_reach_fwd = L1 + L2 
        max_reach_bck = L1 - L2 
        print(np.sqrt(x**2 + y**2))
        if( np.sqrt(x**2 + y**2) < max_reach_bck or np.sqrt(x**2 + y**2) > max_reach_fwd ):
            
            return ("no solution found","no solution found")
        else:
            beta = np.arccos((L1**2 + L2**2 - x**2 -y**2)/(2*L1*L2))
            alpha = np.arccos((x**2 + y**2 + L1**2 -L2**2)/(2*L1*np.sqrt(x**2 + y**2)))
            gamma = np.arctan2(y,x)
            #if x>0:
            theta1 = gamma - alpha
            theta2 = np.pi - beta
            print("Before, ",theta1*180/np.pi, theta2*180/np.pi)
#            if y>0 and x<0:
            #    theta2=-theta2
             #   theta1=np.pi + theta1
            #if not(y<0 and x>0):
            theta2 = -theta2
            print(theta1+theta2)
            #if (y<0 and x>0):
            #    theta1 = -theta1
            
            if theta1<-1:
                theta1+=2*np.pi
            #elif theta1>4:
            #    theta1-=2*np.pi
            #else:
            #    theta1 = gamma + alpha
            #    theta2 = beta - np.pi 
            #    print('x is negative')
            # print(theta1+theta2)
            return (theta1,theta2)
     #print(trans, "\n", rot, "\n\n")

    
    


if __name__ == '__main__':
    node = inverseKinematics()
