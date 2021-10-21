#!/usr/bin/env python

import numpy as np 
import modern_robotics as mr
import tf

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

def tf2TFM(tf):
    p = np.array([ tf.translation.x, tf.translation.y, tf.translation.z])
    quart2rot = tf.transformations.euler_from_quaternion(tf.rotation)
    rotx = rot2mat([1, 0, 0], quart2rot[0])
    roty = rot2mat([0, 1, 0], quart2rot[1])
    rotz = rot2mat([0, 0, 1], quart2rot[2])

    rotMat = rotx@roy@rotz

    return mr.RptoTrans(rotMat, p)


