#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from fiducial_msgs.msg import FiducialTransformArray
import tf
import modern_robotics as mr
import numpy as np 
import sys

def get_rotation (quart_orientation): 
   return tf.transformations.euler_from_quaternion(quart_orientation)


class tfTransformer:
    def __init__(self):
        current_base = 1
        if (len(sys.argv) > 1):
            current_base = int (sys.argv[1])

        rospy.init_node('listener', anonymous = True)
        
        self.tftl = tf.TransformListener("/fiducials_transforms")
        self.base_fiducial = current_base
        print(self.base_fiducial)

        rospy.Subscriber("/fiducial_transforms", FiducialTransformArray, self.publish_cam_TF)
        self.got_fid_base = False
        rospy.spin()

    def publish_cam_TF(self, msg):
        image_t = msg.header.stamp

        if( self.got_fid_base ):
            #publish tf
            print(self.fiducial_transform)
        else:
            for m in msg.transforms:
                fid_id = m.fiducial_id
                print("current FIDID is: ", fid_id, "read ID id: ", self.base_fiducial)
                if( fid_id == self.base_fiducial ):
                    self.fiducial_transform = m
                    self.got_fid_base = True
                    print(m)    
                else: 
                    print("Error: unable to detect correct fiducial mate u suk")


if __name__ == '__main__':
    node = tfTransformer()
