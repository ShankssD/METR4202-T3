#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from fiducial_msgs.msg import FiducialTransformArray
import tf
import modern_robotics as mr
import numpy as np 

def get_rotation (quart_orientation): 
   return tf.transformations.euler_from_quaternion(quart_orientation)


class tfTransformer:
    def __init__(self):
        
        rospy.init_node('listener', anonymous = True)

        self.tftl = tf.TransformListener("/fiducials_transforms")
        self.base_fiducial = 1
        

        rospy.Subscriber("/fiducial_transforms", FiducialTransformArray, self.newTf)
        self.got_fid_base = False
        rospy.spin()

    def newTf(self, msg):
        image_t =  msg.header.stamp
        print ("\n*********************************************************")

        for m in msg.transforms:
            current_fid_id = m.fiducial_id
            if (current_fid_id == self.base_fiducial):
                if(not self.got_fid_base):
                    self.tf_fid_base = m.transform.translation
                    print(self.tf_fid_base)
                    self.got_fid_base = True
                    print("got Fiducial %d as the base"% self.base_fiducial)

            elif(self.got_fid_base):
                try:
                    now = rospy.Time.now()
                    past = now - rospy.Duration(5.0)
                    
                    tf = self.tftl.lookupTransform(self.tf_fid_base, current_fid_id,now )
                    ct = tf[0]
                    cr = tf[1]

                    print("ID %d rel4" % current_fid_id,"norm: ", norm(ct),"\n translation vector: ", ct, "rotation vector: ", get_rotation(cr))
                except Exception as e:
                    print("Could not find transform with exception of %s" % e)
            else: 
                print("Not yet found base fiducial!")
                return


if __name__ == '__main__':
    node = tfTransformer()
