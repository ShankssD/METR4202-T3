#!/usr/bin/env python  

import rospy
import math
import numpy as np 
import tf2_ros as tf2
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import TransformStamped, Twist
from fiducial_msgs.msg import FiducialTransformArray
from std_msgs.msg import String, Float64
from geometry_msgs.msg import Vector3
from tf2_msgs.msg import TFMessage
from std_msgs.msg import Bool

L1 = 0.120
L2 = 0.095
max_reach = L1 + L2
min_reach = L1 - L2

class publishBlockTF:
    """
    The publishBlockTF class handles the movement and detection of multiple fiducials.
    """
    def __init__ (self):
        rospy.init_node("BlockTransformationPublisher")
        self.pub = rospy.Publisher('availableBlockTransforms',TFMessage,queue_size=1)
        self.conveyorMoving = rospy.Subscriber('/conveyor_rotation', Bool, self.conveyorState)
        self.availableFiducials = rospy.Subscriber("/fiducial_transforms", FiducialTransformArray, self.fiducial_presence)
        self.tfBuffer = tf2.Buffer()
        self.listener = tf2.TransformListener(self.tfBuffer)
        self.rate = rospy.Rate(10.0)
        self.base_fid_ID = 27
        self.isMoving = True

        rospy.spin()

    def fiducial_presence(self, msg):
        """
        The fiducial presence function detects the presence of a fiducial that is not the base fiducial and goes to the first
        reachable one detected.
        @param: msg: A msg variable passed in order to obtain the data required.
        """
        
        if not self.isMoving:
            print("Not moving",self.isMoving)
            for m in msg.transforms:
                current_ID = m.fiducial_id
                if(current_ID != self.base_fid_ID):
            
                    if self.check_reachable(m):
                        transformation = None

                        try:
                            transformation = self.tfBuffer.lookup_transform('fiducial_%d' % self.base_fid_ID\
                                , 'fiducial_%d' % current_ID, rospy.Time(0), rospy.Duration(3.0))
                        except (tf2.LookupException, tf2.ConnectivityException, tf2.ExtrapolationException) as e:
                            print(e)
                            continue

                        if(transformation):
                            data = TFMessage()
                            data.transforms.append(transformation)
                            self.pub.publish(data)
        
    
    def conveyorState(self, conveyorState):
        """
        The conveyor state function obtains a boolean value stating whether the conveyor is moving or not.
        @param: conveyorState: A msg variable passed that gives the conveyor state.
        """
        self.isMoving = conveyorState.data
    
    def get_TF_xyz (self, msg):
        """
        The get TF xyz function obtains and returns the translational x and y values for the current message passed.
        @param: msg: A msg variable passed that gives the TFMessage in order to obtain x and y values. 
        @return: x_pos: The x translational position of the fiducial/block.
        @return: y_pos: The y translational position of the fiducial/block.
        """
        x_pos = msg.transform.translation.x 
        y_pos = msg.transform.translation.y
        return (x_pos, y_pos)

    def check_reachable(self, msg):
        """
        The check reachable function checks if the current position is reachable by the robot and returns a boolean.
        @param: msg: A msg variable in order to obtain the x and y translational positions.
        @return: reachable: A boolean determining whether the block is reachable.
        """
        x,y = self.get_TF_xyz(msg)
               
        if( np.sqrt(x**2 + y**2) > max_reach or np.sqrt(x**2 + y**2) < min_reach ):
            return False
        
        return True 


if __name__ == '__main__':
    tf_pub = publishBlockTF()
