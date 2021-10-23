#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image

def image_data(data):
    
    G = data.data[512*512 + 2]
    R = data.data[512*512 + 1]
    B = data.data[512*512 + 0]

    print("Colours:")
    print("R: ", R)
    print("G: ", G)
    print("B: ", B)

def listener_colour():
    rospy.init_node('listener_colour', anonymous=True)
    rospy.Subscriber('ximea_cam/image_raw', Image, image_data)

    rospy.spin()

if __name__ == "__main__":
    listener_colour()
