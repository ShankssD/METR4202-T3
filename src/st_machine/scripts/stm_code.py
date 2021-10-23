#!/usr/bin/env python

import rospy
from smach import State,StateMachine
import smach_ros
from time import sleep
from std_msgs.msg import Bool,String
from tf2_msgs.msg import TFMessage
from sensor_msgs.msg import JointState
from math import isclose
from geometry_msgs.msg import TransformStamped    

class InitialPosition(State):
    def __init__(self):
        State.__init__(self, outcomes=['atIP'])

        self.pub = rospy.Publisher("/newEffPosition", TFMessage, queue_size = 1)
        self.sub = rospy.Subscriber("/joint_states", JointState, self.atPos)
        print("YESSSSSSS")
        self.isIP = False

    def execute(self, userdata):
        rospy.loginfo('Executing state InitialPosition')
        
        #STATE EXECUTION CODE

        t = TransformStamped()
        t.transform.translation.x = -0.05
        t.transform.translation.y = 0.164
        initialPos = TFMessage([t])
        print(initialPos) 
        self.pub.publish(initialPos)
        

        while(not self.isIP):
    
            print("Waiting to reach Intialpos")
        print("zozozozoz")
        return 'atIP'

    def atPos(self, msg):
        print("FUCK YOU", msg)
        pos = msg.position
        joint1pos = 1.57
        joint2pos = 0
        joint3pos = 0
        joint4pos = 0
        if (isclose(pos[3], joint1pos,abs_tol= 0.2) and isclose(pos[2], joint2pos,abs_tol= 0.2)\
             and isclose(pos[1],joint3pos,abs_tol= 0.2) and isclose(pos[0],joint4pos,abs_tol= 0.2)):
            print(self.isIP)
            self.isIP = True

class WaitforBlock(State):
    def __init__(self):
        State.__init__(self,outcomes=['blockFound'], output_keys=['detectedPosition'])
        self.sub = rospy.Subscriber('/availableBlockTransforms', TFMessage, self.getTransform)
        self.ignoreTransform = 0
        self.gotTransform = False

    def getTransform(self, msg):
        
        if not self.gotTransform:
            if self.ignoreTransform < 3:
                self.ignoreTransform += 1
            else:
                self.blockTransform = msg
                self.gotTransform = True
    
    def execute(self,userdata):
        rospy.loginfo('Executing state MovetoBlock')
        while not self.gotTransform :
            print("Waiting for transform",self.gotTransform)
        print("Transform recieved is: ")
        print(self.blockTransform)
        userdata.detectedPosition = self.blockTransform
        return 'blockFound'

class MovetoBlock(State):
    def __init__(self):
        State.__init__(self,outcomes=['atBlock'], input_keys=['blockPosition'])
        self.aboveBlock = False
        self.gotPos = False
        self.can_get_pos = False
        self.desired_position = []
        self.pub = rospy.Publisher("/newEffPosition", TFMessage, queue_size = 1)
        self.sub = rospy.Subscriber("/joint_states", JointState, self.atPos)
        self.desired = rospy.Subscriber("/desired_joint_states",JointState,self.rqPos)



    def execute(self,userdata):
        rospy.loginfo('Executing state MovetoBlock')

        requiredPos = userdata.blockPosition #COMES FROM MOVETOBLOCK
        print(requiredPos)
        self.pub.publish(requiredPos)
        self.can_get_pos = True
        while(not self.gotPos):
            print('Waiting for Block Position')
        while(not self.aboveBlock):
            print("Not yet at position")

        return 'atBlock'
    
    def atPos(self, msg):
        if(self.gotPos):
            pos = msg.position 
            joint1pos = self.desired_position[0]
            joint3pos = self.desired_position[1]
            joint4pos = self.desired_position[2]

            if (isclose(pos[3], joint1pos,abs_tol= 0.2)\
                and isclose(pos[1],joint3pos,abs_tol= 0.2)\
                    and isclose(pos[0],joint4pos,abs_tol= 0.2)):
                
                self.aboveBlock = True
    
    def rqPos(self,msg):
        if self.can_get_pos:
            pos = msg.position
            print(len(pos))
            if(len(pos) == 3):
                for i in range(len(pos)):
                    self.desired_position.append(pos[i])
                print("FUCK")
                self.gotPos = True
            


class GripBlock(State):
    def __init__(self):
        State.__init__(self,outcomes=['gripped'])
        self.desired_height = rospy.Publisher('set_height_state',Bool,queue_size=10)
        self.gripperstate = rospy.Publisher('gripper_actuate',String,queue_size=10)
        self.sub = rospy.Subscriber("/joint_states", JointState, self.atPos)
        self.grip = rospy.Subscriber('gripper_state',String,self.closed)

        self.gotHeight = False
        self.downHeight = False
        self.upHeight = False
        self.isClosed = False
        
    def execute(self,userdata):
        rospy.loginfo('Executing state GripBlock')
   
        self.desired_height.publish(False)

        while (not self.downHeight):
            print("Waiting to go down")

        self.gripperstate.publish('CLOSE')
        while (not self.isClosed):
            print("Waiting to close")

        self.desired_height.publish(True)
        while (not self.upHeight):
            print("Waiting to go up")
        
        return 'gripped'
    
    def atPos(self,msg):
        pos = msg.position
        if isclose(pos[2],-2,abs_tol=0.2):
            self.downHeight = True
            self.upHeight = False
        if isclose(pos[2],2,abs_tol=0.2):
            self.upHeight = True
            self.downHeight = False
    
    def closed(self,msg):
        rospy.sleep(1)
        self.isClosed =True


     

class DropBlock(State):
    def __init__(self):
        State.__init__(self,outcomes=['dropped'])
        self.desired_height = rospy.Publisher('set_height_state',Bool,queue_size=10)
        self.gripperstate = rospy.Publisher('gripper_actuate',String,queue_size=10)
        self.sub = rospy.Subscriber("/joint_states", JointState, self.atPos)
        self.grip = rospy.Subscriber('gripper_state',String,self.opened)

        self.gotHeight = False
        self.downHeight = False
        self.upHeight = False
        self.isOpen = False
        
    def execute(self,userdata):
        rospy.loginfo('Executing state GripBlock')
   
        self.desired_height.publish(False)

        while (not self.downHeight):
            print("Waiting to go down")

        self.gripperstate.publish('OPEN')
        while (not self.isOpen):
            print("Waiting to open")

        self.desired_height.publish(True)
        while (not self.upHeight):
            print("Waiting to go up")
        
        return 'dropped'
    
    def atPos(self,msg):
        pos = msg.position
        if isclose(pos[2],-2,abs_tol=0.2):
            self.downHeight = True
            self.upHeight = False
        if isclose(pos[2],2,abs_tol=0.2):
            self.upHeight = True
            self.downHeight = False
    
    def opened(self,msg):
        sleep(1)
        self.isOpen =True

class MovetoDZ(State):
    def __init__(self):
        State.__init__(self,outcomes=['atDZ'])
        self.counter = 1
        self.desired_position =[]
        self.atDZ = False
        self.gotPos = False
        self.can_get_pos = False
        self.pub = rospy.Publisher('newEffPosition',TFMessage,queue_size=1)
        self.sub = rospy.Subscriber("/joint_states", JointState, self.atPos)
        self.desired = rospy.Subscriber("/desired_joint_states",JointState,self.rqPos)
 


    def execute(self, userdata):
        rospy.loginfo('Executing state MovetoDZ')
        t = TransformStamped()
 
        if self.counter % 4 == 1:
            x = -0.05
            y = 0.15

        elif self.counter % 4 == 2:
            x = -0.15
            y = 0.05

        elif self.counter % 4 == 3:
            x = -0.15
            y = -0.05
        else:
            x = -0.05
            y = -0.15

        t.transform.translation.x = x
        t.transform.translation.y = y  
        currentPos = TFMessage([t]) 
        self.pub.publish(currentPos)
        self.can_get_pos = True
        self.counter += 1

        while(not self.gotPos):
            print('Geting position')
        while(not self.atDZ):
            print('Going to DZ')

        return 'atDZ'
    
    def atPos(self, msg):
        if(self.gotPos):
            pos = msg.position
            joint1pos = self.desired_position[0]
            joint2pos = self.desired_position[1]
            joint3pos = self.desired_position[2]
            joint4pos = self.desired_position[3]
            if (isclose(pos[0], joint1pos,abs_tol= 0.2)\
                and isclose(pos[1], joint2pos,abs_tol= 0.2)\
                and isclose(pos[2],joint3pos,abs_tol= 0.2)\
                    and isclose(pos[3],joint4pos,abs_tol= 0.2)):
                
                self.atDZ = True
    
    def rqPos(self,msg):
        if self.can_get_pos:
            pos = msg.position
            for i in range(len(pos)):
                self.desired_position.append(pos[i])
            self.gotPos = True

def main():
    rospy.init_node("RobotStateMachine")

    sm = StateMachine(outcomes=['grip'])
    sm.userdata.sm_blockPosition = None
    with sm:
        StateMachine.add('InitialPosition', InitialPosition(), transitions={'atIP':'WaitforBlock'})
        StateMachine.add('WaitforBlock', WaitforBlock(), transitions = {'blockFound':'MovetoBlock'}, remapping={'detectedPosition':'sm_blockPosition'})
        StateMachine.add('MovetoBlock', MovetoBlock(), transitions={'atBlock':'GripBlock'}, remapping={'blockPosition':'sm_blockPosition'})
        StateMachine.add('GripBlock', GripBlock(), transitions={'gripped':'MovetoDZ'})
        StateMachine.add('MovetoDZ', MovetoDZ(), transitions = {'atDZ':'DropBlock'})
        StateMachine.add('DropBlock', DropBlock(), transitions={'dropped':'InitialPosition'})

    outcome = sm.execute()
    rospy.spin()

if __name__ == '__main__':
    try: 
        main()
    except rospy.ROSInterruptException:
        rospy.loginfo("Task Completed")