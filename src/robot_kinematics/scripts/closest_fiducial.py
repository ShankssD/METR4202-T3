#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from fiducial_msgs.msg import FiducialTransformArray
import tf
from numpy.linalg import norm

def get_rotation (quart_orientation): 
    orientation_list = [quart_orientation.x,\
                        quart_orientation.y,\
                        quart_orientation.z,\
                        quart_orientation.w]
    return tf.transformations.euler_from_quarternion(orientation_list)

class tfTransformer:
    def __init__(self):
        
        rospy.init_node('listener', anonymous = True)

        self.tftl = tf.TransformListener("/fiducials_transforms")
        self.base_fiducial = 6
        

        rospy.Subscriber("/fiducial_transforms", FiducialTransformArray, self.newTf)
        self.got_fid_target = False
        rospy.spin()

    def newTf(self, msg):
        image_t =  msg.header.stamp
        print ("******")

        for m in msg.transforms:
            current_fid = m.fiducial_id    
            if (m.fiducial_id == self.base_fiducial):
                self.target_fid = m
                self.got_fid_target = True
                print("got Fiducial %d as the base"% self.base_fiducial)

            elif(self.got_fid_target):
                try:
                    tf = self.tftl.lookupTransform("/fiducial_%d" % self.base_fiducial,"/fiducial_%d" % current_fid,rospy.Time(0))
                    ct = tf[0]
                    cr = tf[1]
                    print(ct)
#                    print("norm: ", norm(ct),"\n translation vector: ", ct, "rotation vector: ",get_rotation(cr))
                except Exception as e:
                    print ("Could not get tf for %s with %s " %( m.fiducial_id,e) )
                


            else: 
                print("Not yet found base fiducial!")
                return


if __name__ == '__main__':
    node = tfTransformer()
