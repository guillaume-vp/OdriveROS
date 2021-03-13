#!/usr/bin/env python
import rospy
from std_msgs.msg import Int32, String

import odrive
from odrive.enums import *

from time import sleep

class odrive_motors:

    def __init__(self):
        self.od0 = odrive.find_any()

        self.axis_left = self.od0.axis0
        self.axis_right = self.od0.axis1
        self.con_left = self.axis_left.controller
        self.con_right = self.axis_right.controller

        self.vel = 1

        if self.axis_left.current_state != AXIS_STATE_CLOSED_LOOP_CONTROL:
            self.Initialisation(self.axis_left, "Left Axis")

        if self.axis_right.current_state != AXIS_STATE_CLOSED_LOOP_CONTROL:
            self.Initialisation(self.axis_right, "Right Axis")

        sleep(1)
        self.con_left.input_vel = 0
        self.con_right.input_vel = 0
        rospy.loginfo("Ready")
    

    def Initialisation(self, axis, name):
        
        rospy.loginfo(name + ": Starting Calibration")
        axis.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
        
        while axis.current_state != AXIS_STATE_IDLE:
            sleep(0.1)
        
        axis.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

    def Move(self,data):
        if data.data == 'space':
            self.con_left.input_vel = 0
            self.con_right.input_vel = 0
            rospy.loginfo("I heard %s", data.data)
        
        elif data.data == 'up':
            self.con_left.input_vel =  2 * self.vel
            self.con_right.input_vel = -2 * self.vel
            rospy.loginfo("I heard %s", self.con_left.input_vel)

        elif data.data == 'down':
            self.con_left.input_vel =  -2 * self.vel
            self.con_right.input_vel =  2 * self.vel
            rospy.loginfo("I heard %s", data.data)
                
        elif data.data == 'right':
            self.con_left.input_vel = 2 * self.vel
            self.con_right.input_vel = -1 * self.vel

        elif data.data == 'left':
            self.con_left.input_vel = 1 * self.vel
            self.con_right.input_vel = -2 * self.vel

        elif data.data == 'z':
            if self.vel < 5 :
                self.vel += 1
                for con in [self.con_left, self.con_right]:
                    con.input_vel = con.input_vel / (self.vel-1) * self.vel

        elif data.data == 's':
            if self.vel > 1:
                self.vel -= 1
                for con in [self.con_left, self.con_right]:
                    con.input_vel = con.input_vel / (self.vel+1) * self.vel        


def callback(data, od):
    
    #rospy.loginfo("I heard %s", data.data)
    #rospy.loginfo("I heard %s", od.vel)
    od.Move(data)



if __name__ == '__main__':
    rospy.init_node('vel_listener')
    od = odrive_motors()
    rospy.Subscriber("odrive_input_direction", String, callback, od)
    rospy.spin()