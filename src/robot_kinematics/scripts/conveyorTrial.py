#!/usr/bin/env python  
import numpy as np
import rospy
from tf2_msgs.msg import TFMessage
from math import isclose
from std_msgs.msg import Bool
from fiducial_msgs.msg import FiducialTransformArray
import tf
L1 = 0.120
L2 = 0.095
max_reach = L1 + L2
min_reach = L1 - L2


class conveyorMovement(): 
    """
    A class to check the movement of the conveyor belt on which the boxes are placed.
    """
    def __init__ (self):
        rospy.init_node('conveyor_state')
        self.sub = rospy.Subscriber("/fiducial_transforms", FiducialTransformArray,self.conveyor_state, queue_size = 1)
        self.pub = rospy.Publisher("/conveyor_rotation", Bool, queue_size=1)
        self.previousFidTF = None
        self.previousFidID = None
        self.baseFidID = 27
        self.isMoving = True 
        self.rotationTol = 0.02
        self.transTol = 0.02
        self.checkCounter = 0
        self.ignoreCall = False
        self.rate = rospy.Rate(10)
        rospy.spin()

    def conveyor_state(self, msg):
        """
        The conveyor state function checks and publishes the current state of the conveyor.
        @param: msg: A String variable called from the fiducial transforms.
        """
            
        print("called")
        print(msg)
        for m in msg.transforms:
            currentFidID = m.fiducial_id

            print("Difference:", currentFidID != self.baseFidID)
            if(self.previousFidID == None):
                #save TF        
                if currentFidID != self.baseFidID:

                    self.previousFidID = currentFidID
                    self.get_TF_data(m)

            else:
                print(self.previousFidID)
                if(currentFidID == self.previousFidID):

                    currentTrans = self.get_TF_xyz(m)
                    sameTF = True#False 

                    for current, previous in zip(currentTrans, self.previousFidTrans):
                        if( not isclose(current, previous, abs_tol = self.transTol)): 
                            sameTF = False
                            print("Conveyor Moving")
                            break
                    if sameTF == True:
                        self.checkCounter += 1
                    else:
                        print("Conveyor Moving")
                        self.isMoving = True

                    if (self.checkCounter == 2):
                        self.isMoving = False
                        print("Counter 3 and conveyor not moving with FID: ", currentFidID)
                        self.checkCounter = 0    
                    elif (not sameTF):
                        print("reset")
                        self.isMoving = True
                        self.checkCounter = 0
                    self.get_TF_data(m)
            self.pub.publish(self.isMoving)
        self.rate.sleep()
    
    def get_TF_data(self, msg):
        """
        The get TF data function gets the transformation data as is.
        @param: msg: A string variable called from the fiducial transforms.
        """
        self.previousFidTrans = self.get_TF_xyz(msg)
        self.previousFidTF = msg     

    def get_TF_eulz (self, msg):
        """
        The get TF data eulz function gets the transformation data and converts from quarternion
        to euler.
        @param: msg: A string variable called from the fiducial transforms.
        @return: rot_z: Rotation about the z axis.
        """
        quart_xyzw = msg.transform.rotation
        rot_mat = tf.transformations.euler_from_quaternion([quart_xyzw.x, quart_xyzw.y, \
            quart_xyzw.z, quart_xyzw.w]) 
        return rot_mat[2]

    def get_TF_xyz (self, msg):
        """
        The get TF xyz function gets the translation data from the transform and returns it.
        @param: msg: A string variable called from the fiducial transforms.
        @return: x_pos: The integer value of the translation in x.
        @return: y_pos: The integer value of the translation in y.
        """
        x_pos = msg.transform.translation.x 
        y_pos = msg.transform.translation.y
        return (x_pos, y_pos)



if __name__ == "__main__":

    bid = conveyorMovement()
 
