#!/usr/bin/env python
from __future__ import print_function

from time import sleep

from pynput import keyboard
from pynput.keyboard import Key

import rospy
import std_msgs.msg
from std_msgs.msg import String

class KeyPressMonitor:

    def __init__(self):
        self.pub = rospy.Publisher('odrive_input_direction', String, queue_size=10)
        self.rate = rospy.Rate(5)
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press)
        self.keyboard_listener.start()

    def on_press(self, key):
        keyChar= 'aaa'
        try:
            keyChar = key.char           

    
        except AttributeError :
            if key == Key.up:
                keyChar = 'up'
            elif key == Key.down: 
                keyChar = 'down'
            elif key == Key.right:
                keyChar = 'right'
            elif key == Key.left:
                keyChar = 'left'

            elif key == Key.esc:
                self.keyboard_listener.stop()
                sleep(1)
                rospy.signal_shutdown("Manual shutdown")
                return False
            elif key == Key.space:
                keyChar = 'space'

        finally:
            rospy.loginfo(keyChar)
            self.pub.publish(keyChar)


    def stop(self):
        self.keyboard_listener.stop()



if __name__ == '__main__':
    try:
        rospy.init_node('vel_talker')
        kpm = KeyPressMonitor()
        rospy.on_shutdown(kpm.stop)
        rospy.spin()
    
    except rospy.ROSInterruptException:
        pass