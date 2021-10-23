#!/usr/bin/env python  
import roslib
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


if __name__ == '__main__':
    rospy.init_node('fiducial_listener')
    
    data_pub = rospy.Publisher('availableBlockTransforms',TFMessage,queue_size=10)
    tfBuffer = tf2.Buffer()
    listener = tf2.TransformListener(tfBuffer)
    
    rate = rospy.Rate(100.0)
    while not rospy.is_shutdown():
        transformation = None
        try:
            transformation = tfBuffer.lookup_transform('fiducial_3', 'fiducial_7', rospy.Time(0), rospy.Duration(3.0))
            print(type(transformation))
        except (tf2.LookupException, tf2.ConnectivityException, tf2.ExtrapolationException) as e:
           print(e)
           continue

        if(transformation):
            translation_data = transformation.transform.translation
            print(translation_data)
            offset_translation_data = np.array([translation_data.x +0.05, translation_data.y +0.05])
            rot_mat = transformation.transform.rotation
            rotation_data_rad = euler_from_quaternion(np.array([rot_mat.x, rot_mat.y, rot_mat.z, rot_mat.w]))
            rotation_data_deg = np.zeros(3)
            for n in range(0,3):
                rotation_data_deg[n] = rotation_data_rad[n]*180/np.pi #change to degrees()
            print("\n\n Transformation translation: \n", offset_translation_data, "\nRotation z:\n", rotation_data_deg[2])
            data = TFMessage()
            data.transforms.append(transformation)
            data_pub.publish(data)

        rate.sleep()
