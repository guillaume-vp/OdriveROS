#!/usr/bin/env python
import rospy
from std_msgs.msg import Int32,String

import time

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    

if __name__ == '__main__':
    rospy.init_node('vel_listener')

    rospy.Subscriber("odrive_input_direction", String, callback)
    rospy.spin()