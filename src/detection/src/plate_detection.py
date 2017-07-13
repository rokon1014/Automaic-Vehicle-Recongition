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


bridge = CvBridge()
car_cascade = cv2.CascadeClassifier('/home/rokon/catkin_ws/src/detection/src/plate_cascade/cascade1.xml')
def callback(data):
	try:
		cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
		gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
		car = car_cascade.detectMultiScale(gray, 1.02, 25)
		index=1

	

	  	for (x,y,w,h) in car:

	  		if w>100 and h>100:
			    cv2.rectangle(cv_image,(x,y),(x+w,y+h),(255,0,0),2)
			    roi_gray = gray[y:y+h, x:x+w]
			    roi_color = cv_image[y:y+h, x:x+w]

			    cropped = cv_image[y :y +  h , x : x + w] 
			    s =  str(index) + '.jpg'
			    #cv2.imshow(s , cropped)
			    #cv2.waitKey(0)    
			    index = index + 1
			    print "inside"
			    image_pub.publish(bridge.cv2_to_imgmsg(cropped, "bgr8"))
			    image_pub_test.publish("testing")








		cv2.imshow('new',cv_image)
		cv2.waitKey(0)    


	except CvBridgeError as e:
	   print(e)


rospy.init_node('plateDetection', anonymous=False)
image_sub = rospy.Subscriber("carDetected",Image, callback)
image_pub = rospy.Publisher("plate_detected",Image)
image_pub_test = rospy.Publisher("plateDetected", String, queue_size=10)


rospy.spin()