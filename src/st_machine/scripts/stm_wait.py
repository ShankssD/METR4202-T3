#!/usr/bin/env python

import rospy
from smach import State,StateMachine
from time import sleep
from std_msgs.msg import String
from tf2_msgs.msg import TFMessage
from math import isclose
from geometry_msgs.msg import TransformStamped    

class InitialPosition(State):
    def __init__(self):
        State.__init__(self, outcomes=['atIP'])

        self.t = TransformStamped()
        self.t.transform.translation.x = -0.05
        self.t.transform.translation.y = 0.165
        self.initialPos = TFMessage([self.t])
       
        self.pub = rospy.Publisher("/newEffPosition", TFMessage, queue_size = 10)
        self.desired_height = rospy.Publisher('/set_height_state',String,queue_size=10)
        self.gripperstate = rospy.Publisher('/gripper_actuate',String,queue_size=10)

        self.isIP = False

    def execute(self, userdata):
        rospy.loginfo('Executing state InitialPosition')
        
        #STATE EXECUTION CODE
        while(self.pub.get_num_connections() < 1):
            rospy.sleep(1)
        self.pub.publish(self.initialPos)

        rospy.loginfo("Getting to Initial Position at:")
        print(self.initialPos)

        rospy.sleep(5.)

        while(self.desired_height.get_num_connections() <1 or self.gripperstate.get_num_connections() < 1):
                rospy.sleep(1)

        self.desired_height.publish("UP")        
        self.gripperstate.publish('OPEN')

        rospy.sleep(5.)

        return 'atIP'


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
        self.ignoreTransform = 0
        self.gotTransform = False
        counter = 0
        while not self.gotTransform :
            rospy.loginfo("Waiting for transform: ")
            print(self.gotTransform)
            rospy.sleep(2)

        rospy.loginfo("Transform recieved")
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

        self.pub = rospy.Publisher("/newEffPosition", TFMessage, queue_size = 10)

    def execute(self,userdata):
        rospy.loginfo('Executing state MovetoBlock')

        requiredPos = userdata.blockPosition #COMES FROM MOVETOBLOCK
        rospy.loginfo("TARGET ACQUIRED")
        print(requiredPos)

        while (self.pub.get_num_connections() < 1):
            rospy.sleep(1)

        self.pub.publish(requiredPos)

        self.can_get_pos = True
        
        rospy.sleep(4)

        return 'atBlock'

            


class GripBlock(State):
    def __init__(self):
        State.__init__(self,outcomes=['gripped'])
        self.desired_height = rospy.Publisher('/set_height_state',String,queue_size=10)
        self.gripperstate = rospy.Publisher('/gripper_actuate',String,queue_size=10)

        self.gotHeight = False
        self.downHeight = False
        self.upHeight = False
        self.isClosed = False
        
    def execute(self,userdata):
        rospy.loginfo('Executing state GripBlock')
        
        while(self.desired_height.get_num_connections() <1 or self.gripperstate.get_num_connections() < 1):
            rospy.sleep(1)


        self.desired_height.publish("DOWN")

        rospy.sleep(5)


        self.gripperstate.publish('CLOSE')


        rospy.sleep(3)

        self.desired_height.publish("UP")
        
        rospy.sleep(5)

        return 'gripped'



     

class DropBlock(State):
    def __init__(self):
        State.__init__(self,outcomes=['dropped'])
        self.desired_height = rospy.Publisher('/set_height_state',String,queue_size=10)
        self.gripperstate = rospy.Publisher('/gripper_actuate',String,queue_size=10)


        
    def execute(self,userdata):
        rospy.loginfo('Executing state DropBlock')

        while(self.desired_height.get_num_connections() <1 or self.gripperstate.get_num_connections() < 1):
            rospy.sleep(1)

        self.desired_height.publish('DOWN')
        rospy.sleep(5)


        self.gripperstate.publish('OPEN')
        rospy.sleep(3)


        self.desired_height.publish('UP')        
        rospy.sleep(5)

        
        return 'dropped'
    


class MovetoDZ(State):
    def __init__(self):
        State.__init__(self,outcomes=['atDZ'])
        self.counter = 1
        self.desired_position =[]
        self.atDZ = False
        self.gotPos = False
        self.can_get_pos = False
        self.pub = rospy.Publisher('newEffPosition',TFMessage,queue_size=10)

 


    def execute(self, userdata):
        rospy.loginfo('Executing state MovetoDZ')
        t = TransformStamped()
        base_offset = 0.05
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

        t.transform.translation.x = x - base_offset
        t.transform.translation.y = y - base_offset
        currentPos = TFMessage([t]) 

        while(self.pub.get_num_connections() < 1):
            rospy.sleep(1)

        self.pub.publish(currentPos)
        self.can_get_pos = True
        self.counter += 1

        sleep(3)


        return 'atDZ'
    
def main():
    rospy.init_node("RobotStateMachine")

    sm = StateMachine(outcomes=['dropped'])
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
    except (rospy.ROSInterruptException, KeyboardInterrupt):
        rospy.loginfo("Task Completed")
