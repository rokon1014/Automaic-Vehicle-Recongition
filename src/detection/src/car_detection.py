#!/usr/bin/env python


import rospy
import numpy as np
import cv2
from matplotlib import pyplot as plt
import roslib
roslib.load_manifest('detection')
import sys
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError


def callback(data):
    print data.data


car_cascade = cv2.CascadeClassifier('/home/rokon/catkin_ws/src/detection/src/cascade.xml')


img = cv2.imread('/home/rokon/catkin_ws/src/detection/src/test2.jpg')
img = cv2.resize(img, (900, 600))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

car = car_cascade.detectMultiScale(gray, 1.31, 70)
index=1
print car
for (x,y,w,h) in car:

	if w>160 and h>160: 

	    #cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
	    roi_gray = gray[y:y+h, x:x+w]
	    roi_color = img[y:y+h, x:x+w]

	    cropped = img[y :y +  h , x : x + w]
	    s =  str(index) + '.jpg' 
	    cv2.imwrite(s, cropped)
	    index = index + 1

bridge = CvBridge()
bridge.cv2_to_imgmsg(cropped, "bgr8")


rospy.init_node('carDetection', anonymous=False)
rospy.Subscriber("imageKinect", String, callback)


image_pub = rospy.Publisher("carDetected",Image)
rate = rospy.Rate(1000)

while(True):
	image_pub.publish(bridge.cv2_to_imgmsg(cropped, "bgr8"))
	
	rate.sleep()








    
cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
