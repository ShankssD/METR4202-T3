import irospy
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist
import numpy as np

class InverseKinematics:
    """
    The class that calculates the Inverse Kinematics of the robot.
    """
    
    def __init__(self, Slist, thetaguess):
        self.Slist = Slist
        self.thetas = thetaguess
        
        self.init_z = 0.05 #The height from base to dynamixel in m.
        
        #NEED TO HARDCODE ALL LINK LENGTHS ETC HERE
        length1 = yes 
        
        #Publishers:
        #First publisher controls base movement
        #CHECK IF PUBLISHERS FINE
        self.base_publisher = rospy.Publisher(
        '/project/base_link_controller/command', Float64, queue_size = 10)
        
        self.link1_publisher = rospy.Publisher(
        '/project/link_1_controller/command', Float64, queue_size = 10)
        
        self.link2_publisher = rospy.Publisher(
        '/project/link_2_controller/command', Float64, queue_size = 10)
        
        self.link3_publisher = rospy.Publisher(
        '/project/link_3_controller/command', Float64, queue_size = 10)
        
        self.gripper_publisher =  rospy.Publisher(
        '/project/gripper_controller/command', Float64, queue_size = 10)
        
        #Subscriber:
        self.desired_pos = rospy.Subscriber(
        '/desired_position', Twist, self.ik_calcs)
        
    def ik_calcs(self):
        """
        The actual calculation for the ik.
        """
        
        #Get the x, y and z coords.
        x = msg.linear.x
        y = msg.linear.y
        z = msg.linear.z
        
        # DEFINE DX DY AND DZ HERE
        
        theta1 = np.arctan(dy, dx) #Theta 1 calculation for the robot
        theta2 = np.arccos(((x**2 + y**2) - (length1**2 + length2**2)) 
                    / (2*length1*length2))




def main():
    while not ctrl_c:
        base = self.base_publisher.get_num_connections()
        link1 = self.link1_publisher.get_num_connections()
        link2 = self.link2_publisher.get_num_connections()
        link3 = self.link3_publisher.get_num_connections()  
        grip = self.gripper_publisher.get_num_connections()  
        
        if(base > 0 and link1 > 0 and link2 > 0 and link3 > 0 and grip > 0):
            self.base_publisher.publish(theta1)
            #DO THIS OVER AND OVER     

if __name__ == '__main__':
    rospy.init_node('InverseKinematics')
    InverseKinematics()
    rospy.spin()
        
