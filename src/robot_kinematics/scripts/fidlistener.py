#!/usr/bin/env python  
import roslib
roslib.load_manifest('learning_tf')
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
    fiducial_pos  = rospy.Publisher('fidpos', geometry_msgs.msg.Vector3Stamped,queue_size=1)

    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        try:
            (trans,rot) = listener.lookupTransform('fid03', '/fid01', rospy.Time(0))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue

        print(trans,rot)

        rate.sleep()
