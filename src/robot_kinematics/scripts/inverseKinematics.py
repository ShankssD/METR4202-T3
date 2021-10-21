#! /usr/bin/env python

import rospy
import numpy as np 
from tf2_msgs.msg import TFMessage
from sensor_msgs.msg import JointState 

L1 = 0.120 
L2 = 0.095


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

        theta1,theta2 = self.required_horiz_joint_angles(x_pos,y_pos)
        pub_msg = JointState()
        pub_msg.name = ['joint_1', 'joint_2']
        pub_msg.position = [theta1, theta2]
        self.pub.publish(pub_msg)



    def required_horiz_joint_angles (self, x,y):
        max_reach_fwd = L1 + L2
        max_reach_bck = L1 - L2
        if( np.sqrt(x**2 + y**2) < max_reach_bck or np.sqrt(x**2 + y**2) > max_reach_fwd ):
            print("no solution found")
            return(0,0)
        else: 
        
            beta = np.arccos((L1**2 + L2**2 - x**2 -y**2)/(2*L1*L2))
            alpha = np.arccos((x**2 + y**2 + L1**2 -L2**2)/(2*L1*np.sqrt(x**2 + y**2)))
            gamma = np.arctan2(y,x)
            
            theta1 = gamma - alpha
            theta2 = np.pi - beta

            return (theta1, theta2)
    
    def get_prismatic_joint_angle (self, height_reqd, current_joint_angle):
        spool_radius  = (27.3**10^(-3))/2
        delta_angle = height_reqd/spool_radius

        new_joint_angle = current_joint_angle + delta_angle
        if(new_joint_angle < -2*np.pi or new_joint_angle > -2*np.pi): #will have to tune this to the current setup
            print("Prismatic distance too low")
            return
        else:
            return (current_joint_angle+delta_angle)

if __name__ == '__main__':
    node = inverseKinematics()
