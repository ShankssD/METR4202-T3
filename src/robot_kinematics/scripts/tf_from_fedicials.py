#!/usr/bin/env python

import rospy
from std.msgs import String
from fiducial_msgs.msg import FiducialTransformArray
import tf
import modern_robotics as mr
import numpy as np
import sys

def trajectory_generation(fiducial):
    
    trajectory =
    pub.(trajectory)
if __name__ == '__main__':
    rospy.Subscriber("/fiducial_transforms:", FiducialTransformArray,trajectory_generation)
    pub = rospy.Publisher('trajectory',
