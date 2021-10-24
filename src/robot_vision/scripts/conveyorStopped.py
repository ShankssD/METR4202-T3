import rospy
from fiducial_msgs.msg import FiducialArray
class CurrentImage:

    def __init__(self,fidcuial_value):
        sub = rospy.Subscriber('/fiducial_verices',FiducialArray,self.current_pos)
