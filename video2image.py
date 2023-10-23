import numpy as np 
import cv2 
cap = cv2.VideoCapture("rtsp://192.168.9.37:8554/all_video.264")
i = 0
while(cap.isOpened()): 
    i += 1
    ret, frame = cap.read()
    if i % 50 == 0:
	    cv2.imwrite("/Users/sonny_he/Desktop/opencv_learning/pictures/test_{}.png".format(i),frame) 

cap.release() 
cv2.destroyAllWindows() 
