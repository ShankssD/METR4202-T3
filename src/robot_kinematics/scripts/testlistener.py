#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from fiducial_msgs.msg import FiducialTransformArray
import tf
from numpy.linalg import norm
import modern_robotics as mr
import numpy as np
from rospy.numpy_msg import numpy_msg
from rospy_tutorials.msg import Floats


def rot2mat (x, theta):
    a1 = np.cos(theta) + (x[0]**2)*(1-np.cos(theta));
    a2 = x[0]*x[1]*(1-np.cos(theta)) + x[2]*np.sin(theta);
    a3 = x[0]*x[2]*(1-np.cos(theta)) - x[1]*np.sin(theta);
    b1 = x[0]*x[1]*(1-np.cos(theta)) - x[2]*np.sin(theta);
    b2 = np.cos(theta) + (x[1]**2)*(1-np.cos(theta));
    b3 = x[1]*x[2]*(1-np.cos(theta))+x[0]*np.sin(theta);
    c1 = x[0]*x[2]*(1-np.cos(theta)) + x[1]*np.sin(theta);
    c2 = x[1]*x[2]*(1-np.cos(theta))- x[0]*np.sin(theta);
    c3 = np.cos(theta) + (x[2]**2)*(1-np.cos(theta));

    return np.array([[a1, b1, c1], [a2, b2, c2], [a3 , b3, c3]])

def tf2TFM(transform):
    p = np.array([ transform.translation.x, transform.translation.y, transform.translation.z])
    print(p)
    r = np.array([ transform.rotation.x, transform.rotation.y, transform.rotation.z, transform.rotation.w])
   
    quart2rot = tf.transformations.euler_from_quaternion(r)
    rotx = rot2mat([1, 0, 0], quart2rot[0])
    roty = rot2mat([0, 1, 0], quart2rot[1])
    rotz = rot2mat([0, 0, 1], quart2rot[2])

    rotMat = rotx@roty@rotz

    return mr.RpToTrans(rotMat, p)



def get_rotation (quart_orientation): 
    return tf.transformations.euler_from_quaternion(quart_orientation)


class tfTransformer:
    def __init__(self):
        
        rospy.init_node('camera_base_TFM', anonymous = True)

        self.tftl = tf.TransformListener("/fiducials_transforms")
        self.base_fiducial = 6
        self.aruco_rel_base_TFM = mr.RpToTrans(rot2mat([0, 0, 0], 0),np.array([0,0,0]))
        self.pub = rospy.Publisher("cam_base_TFM", numpy_msg(Floats),queue_size = 10)
        
        rospy.Subscriber("/fiducial_transforms", FiducialTransformArray, self.newTf)
        self.got_fid_target = False
        rospy.spin()

    def newTf(self, msg):
        """     image_t =  msg.header.stamp
        print ("\n*********************************************************")
        """
        for m in msg.transforms:
            current_fid_id = m.fiducial_id
            current_transform = m.transform

            if(self.base_fiducial == current_fid_id):
                self.aruco_rel_cam_TFM =  tf2TFM(current_transform)
                print("cam rel aruco:\n", self.aruco_rel_cam_TFM)

                self.cam_rel_base_TFM = np.dot(np.linalg.inv(self.aruco_rel_cam_TFM),self.aruco_rel_base_TFM)
                self.got_fid_target = True
                print("cam rel base:\n ", self.cam_rel_base_TFM)
                self.pub.publish(self.cam_rel_base_TFM)
            else:
                print("Have not found camera to base transform ")
            if(self.got_fid_target):
                if(self.base_fiducial != current_fid_id):
                    current_aruco_rel_cam =  tf2TFM(current_transform) 
                    current_aruco_rel_base = np.dot(current_aruco_rel_cam, self.cam_rel_base_TFM)
                    # print("For fiducial %d, the transform is: %s" % (current_fid_id, current_aruco_rel_base)) 
                    


if __name__ == '__main__':
    node = tfTransformer()
