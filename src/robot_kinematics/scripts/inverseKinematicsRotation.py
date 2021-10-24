#!/usr/bin/env python

import rospy
import numpy as np 
import tf as tf
import modern_robotics as mr
from tf2_msgs.msg import TFMessage
from sensor_msgs.msg import JointState 
from std_msgs.msg import Bool,String
from math import isclose





#L1 and L2 are SCARA robot link lengths
L1 = 0.120  
L2 = 0.095



class inverseKinematics:

    """
    Inverse kinematics class takes position required from block and plans path
    """

    def __init__(self):

        """
        Initialises communication channels required to run inverse kinematics
        """
        
        rospy.init_node('inverseKinematics', anonymous = True)
        rospy.loginfo('Inverse Kinematics Has Started')
        self.currently_moving = False
        rospy.Subscriber('/newEffPosition', TFMessage, self.analytical_IK)
        self.pub = rospy.Publisher('/desired_joint_states', JointState, queue_size = 1)
        rospy.spin()
        
 

    def analytical_IK(self, msg):

        """
        A callback function, takes position from aruco marker on block and performs transformation
        from reference marker and to see if there is a solution
        @param: msg: A TFMessage providing the required x
        """

        print(msg.transforms)
        msg = msg.transforms[0]
        x_pos = msg.transform.translation.x +0.05
        y_pos = msg.transform.translation.y +0.05
        quart_xyzw = msg.transform.rotation
        rot_mat = tf.transformations.euler_from_quaternion([quart_xyzw.x, quart_xyzw.y, quart_xyzw.z, quart_xyzw.w])
        print(rot_mat[2])
        theta1,theta3,theta4 = self.required_horiz_joint_angles(x_pos,y_pos, rot_mat[2])
        if theta1 == 'no solution found':
            print('NO SOLUTION FOUND')
            
            return None
        
        pub_msg = JointState()
        pub_msg.name = ['joint_1','joint_3', 'joint_4']
        pub_msg.velocity = [1,1,1]
        pub_msg.position = [theta1,theta3,theta4]
        print("IK Results are: ", theta1, theta3, theta4)
        if(not self.currently_moving):
            self.pub.publish(pub_msg)
       


        
    def required_horiz_joint_angles (self, x,y, rot_rel_base):

        """
        Inverse Kinematics calculations for required x,y and end effector rotation
        @param: x: A float denoting x position from base of robot
        @param: y: A float denoting y position from base of robot
        @param: rot_rel_base: A float denoting the rotation required by the end effector
        @return: (theta1,theta2,-theta3): A tuple of the angles to be sent to the dynamixels
        """
        
        max_reach_fwd = L1 + L2 
        max_reach_bck = L1 - L2 
        if (isclose(x,0, abs_tol=0.000002) and isclose(y,0.215, abs_tol=0.000002)):
            return (np.pi/2,0,0)
            #Checks if x,y is close to home position
        if( np.sqrt(x**2 + y**2) < max_reach_bck or np.sqrt(x**2 + y**2) > max_reach_fwd ):
            #Checks if x,y is withing robots workspace 
            return (0,0,0)
       
        else:
            #Computes maths for IK
            beta = np.arccos((L1**2 + L2**2 - x**2 -y**2)/(2*L1*L2))
            alpha = np.arccos((x**2 + y**2 + L1**2 -L2**2)/(2*L1*np.sqrt(x**2 + y**2)))
            gamma = np.arctan2(y,x)

            theta1 = gamma - alpha
            theta2 = np.pi - beta
            
            theta2 = -theta2 #Angle is negated as dynamixel motor is upsidedown

            if theta1 > 0 and theta2 < 0:
                theta3 = rot_rel_base + (-theta2 - theta1)
            else:
                theta3 = rot_rel_base + (-theta2 - (-theta1))


            if theta1<-1:
                theta1+=2*np.pi
            if theta3 < -2:
                theta3+=np.pi
            
            theta3=-theta3 #Angle is negated as dynamixel motor is upside down

            return (theta1,theta2,theta3)

    


if __name__ == '__main__':
    #Creates inverseKinematics object
    node = inverseKinematics()
