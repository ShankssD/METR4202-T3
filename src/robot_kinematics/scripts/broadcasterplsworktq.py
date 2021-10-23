#!/usr/bin/env python

import rospy
import tf2_ros
import geometry_msgs.msg
from tf2_msgs.msg import TFMessage

def publish_TF(data):
    
    tf2Broadcaster = tf2_ros.TransformBroadcaster()
    Stamp = geometry_msgs.msg.TransformStamped()
    Stamp.header.stamp = rospy.Time.now()
    Stamp.header.frame_id  = '0'
    Stamp.child_frame_id = "base_aruco"
    Stamp.transform.translation  = (0.08639819122170858,0.066858953746093,0.9571570733426882 )
    Stamp.transform.rotation = (0.983501114748627 , 0.03546155970686163 ,0.012945244907967744)
    tf2Broadcaster.sendTransform(Stamp)

if __name__  == "__main__":
    rospy.init_node("TFouter")
    rospy.Subscriber('/tf', TFMessage, publish_TF)
    rospy.spin()
