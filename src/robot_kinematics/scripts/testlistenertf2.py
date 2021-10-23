#!/usr/bin/env python  
import roslib
import rospy
import math
import tf2_ros as tf2
from geometry_msgs.msg import TransformStamped, Twist
from fiducial_msgs.msg import FiducialTransformArray
from std_msgs.msg import String, Float64
from geometry_msgs.msg import Vector3

if __name__ == '__main__':
    rospy.init_node('fiducial_listener')
    
    data_pub = rospy.Publisher('newEffPosition',Vector3,queue_size=10)
    tfBuffer = tf2.Buffer()
    listener = tf2.TransformListener(tfBuffer)
    
    rate = rospy.Rate(100.0)
    while not rospy.is_shutdown():
        #trans = None
        #rot = None  
        try:
            trans,rot = tfBuffer.lookup_transform('fiducial_4', 'fiducial_7', rospy.Time(0))
            print(trans, rot)
            rate.sleep()
        except (tf2.LookupException, tf2.ConnectivityException, tf2.ExtrapolationException) as e:
           print(e)
           rate.sleep()
           continue
           
        translation_data = trans.transform.translation
        rotation_data = rot.transform.rotation
        
        data_pub.publish(translation_data)
        rate.sleep()
