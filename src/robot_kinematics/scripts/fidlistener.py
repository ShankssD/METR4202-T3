#!/usr/bin/env python  
import roslib
import rospy
import math
import tf
from geometry_msgs.msg import TransformStamped, Twist
from fiducial_msgs.msg import FiducialTransformArray

def newTf(msg):
    for m in msg.transforms:
        id = m.fiducial_id
        trans = m.transform.translation
        rot = m.transform.rotation
        
        listener = tf.TransformListener()

        t = TransformStamped()
        print(t.child_frame_id)

if __name__ == '__main__':
    rospy.init_node('fiducial_listener')

    listener = tf.TransformListener()

#    fid_current = rospy.Subscriber("/fiducial_transforms", FiducialTransformArray, newTf)
    fiducial_pos  = rospy.Publisher('fidpos', Twist,queue_size=10)

    rate = rospy.Rate(1)
    while not rospy.is_shutdown():
        trans = None
        rot = None
        try:
            (trans,rot) = listener.lookupTransform('/fiducial_0', '/fiducial_1', rospy.Time(0))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException) as e:
           print(e)
           continue

        print(trans, "\n", rot, "\n\n")


        rate.sleep()
