#!/usr/bin/env python
import rospy
from std_msgs.msg import String


def callback(data):
    print data.data



rospy.init_node('database_GSM', anonymous=False)
rospy.Subscriber("licenseNumber", String, callback)

rospy.spin()
